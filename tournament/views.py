from django.shortcuts import render
from django.http import HttpResponse
from .models import Tournament
from .models import TTeam, TMatch, PMatch, Pool, PRound, PaymentOption
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
import math
import random

# Create your views here.
def tournament(request):
    return render(request, 'tournament/tournament.html')

def tournamentbracket(request, tournament_id = Tournament.objects.all().last().pk):

    tournament = Tournament.objects.get(pk = tournament_id)
    if request.method == "POST":

        if 'enable-editing' in request.POST:
            username, password = request.POST["username"], request.POST["password"]
            user = authenticate(username=username, password=password)
            try:
                login(request, user)
            except:
                message = "Not the correct login. Please contact your tournament organizer to get access to score editing."
                return render(request, 'tournament/tournamentbracket.html', {'tournament':tournament, "message":message})


        if 'generate-pools' in request.POST and request.POST["password"] == tournament.password:

             genPools(tournament, request)


        if 'pmatch' in request.POST: #reporting a pools match

            if ((int(request.POST["score1"]) >= 15 or int(request.POST["score2"]) >= 15) and abs(int(request.POST["score1"]) - int(request.POST["score2"])) >= 2):

                current_pool = tournament.pools.get(poolNumber = request.POST["pool"])
                current_round = current_pool.rounds.get(round_number = request.POST["round"])
                current_pmatch = current_round.matches.get(match_number = request.POST["pmatch"])

                if current_pmatch.winner == False:

                    reportPMatch(tournament, request)

                else:
                    updatePMatch(tournament, request)

            else: #Note a valid score
                message = "Not a valid score. One team must have at least 15 and there must be a point difference of 2 or greater"
                return render(request, 'tournament/tournamentbracket.html', {'tournament':tournament, "message":message})


        if 'generate-tournament' in request.POST and request.POST["password"] == tournament.password: #If we are creating the matches

            genTournament(tournament, request)

        if 'match' in request.POST: #we are reporting a tmatch score

            if (int(request.POST["score1"]) >= 2 or int(request.POST["score2"]) >= 2):
                reportTMatch(tournament, request)

            else: #Note a valid score
                message = "Not a valid score. One team must have at least 2 wins"
                return render(request, 'tournament/tournamentbracket.html', {'tournament':tournament, "message":message})

    return render(request, 'tournament/tournamentbracket.html', {'tournament':tournament})

@login_required
def tournamentpayments(request, tournament_id):
    tournament = Tournament.objects.get(pk = tournament_id)

    if request.method =="POST":
        for team in tournament.teams.all():
            if str(team.pk) in request.POST:
                team.paid = True
            else:
                team.paid = False
            team.save()

    return render(request, 'tournament/tournamentpayments.html', {'tournament':tournament})

def previoustournaments(request):
    all_tournaments = Tournament.objects.all()
    return render(request, 'tournament/previoustournaments.html', {'all_tournaments':all_tournaments})

def tournamentsignup(request):
    tournament = Tournament.objects.all().last()
    if request.method == 'POST': #If we add a team
        addteam(request)
    return render(request, 'tournament/tournamentsignup.html', {'tournament':tournament})

def genPools(tournament, request):
    if len(tournament.pools.all()) == 0:
        no_teams = tournament.teams.all().count()
        no_pools = int(request.POST["num-pools"])

        for i in range(no_pools): #create number of pools
            pool = Pool(poolNumber=i+1)
            pool.save()
            tournament.pools.add(pool)

        rand_teams =[]
        for i in range(no_teams): #Create a random array to randomly assign pools
            rand_teams.append(i)
        random.shuffle(rand_teams)

        teams = tournament.teams.all() #randomizes the order of the teams
        pools = tournament.pools.all() #all of the pools
        for i in range(math.ceil(no_teams/no_pools)): #randomly assign teams to pools
            for j in range(no_pools):
                try:
                    team = teams[rand_teams[i*no_pools + j]]
                    pools[j].teams.add(team) #Adds a team based on the random index
                    pools[j].save()
                except:
                    continue

        for i in range(len(pools)):
            genPoolsMatches(tournament.pools.get(poolNumber=i+1))

def reportPMatch(tournament, request):
    current_pool = tournament.pools.get(poolNumber = request.POST["pool"])
    current_round = current_pool.rounds.get(round_number = request.POST["round"])
    current_pmatch = current_round.matches.get(match_number = request.POST["pmatch"])

    if current_pmatch.winner == False:
        team1 = current_pmatch.team1
        team2 = current_pmatch.team2

        current_pmatch.team1_score = int(request.POST["score1"])
        current_pmatch.team2_score = int(request.POST["score2"])
        current_pmatch.winner = True
        current_pmatch.save()


        if current_pmatch.team1_score > current_pmatch.team2_score:
            team1.wins += 1
            team2.losses +=1
        else:
            team1.losses +=1
            team2.wins +=1

        team1.points_for += int(request.POST["score1"])
        team2.points_for += int(request.POST["score2"])
        team1.points_against += int(request.POST["score2"])
        team2.points_against += int(request.POST["score1"])

        team1.point_differential = team1.points_for - team1.points_against
        team2.point_differential = team2.points_for - team2.points_against

        team1.save()
        team2.save()

        #see if we can complete round
        complete_round = True
        matches = current_round.matches.all()
        for i in range(matches.count()):
            if matches[i].winner:
                continue
            else:
                complete_round = False
                break
        if complete_round == True:
            current_round.completed = True
            current_round.save()
        #See if we can complete pool
        if complete_round == True:
            rounds = current_pool.rounds.all()
            complete_pool = True
            for i in range(rounds.count()):
                if rounds[i].completed == True:
                    continue
                else:
                    complete_pool = False
                    break
            if complete_pool == True:
                current_pool.completed = True
                current_pool.save()

            #Check if all pools are completed
            all_pools_complete = True
            pools = tournament.pools.all()
            for i in range(pools.count()):
                if pools[i].completed == True:
                    continue
                else:
                    all_pools_complete = False
                    break
            #If they are all complete, then we can update that
            if all_pools_complete == True:
                tournament.pools_completed = True
                tournament.save()
                #Generate seeding
                genSeeding(tournament)

def updatePMatch(tournament, request):
    current_pool = tournament.pools.get(poolNumber = request.POST["pool"])
    current_round = current_pool.rounds.get(round_number = request.POST["round"])
    current_pmatch = current_round.matches.get(match_number = request.POST["pmatch"])

    team1 = current_pmatch.team1
    team2 = current_pmatch.team2

    team1.points_for -= current_pmatch.team1_score
    team1.points_against -= current_pmatch.team2_score
    team2.points_for -= current_pmatch.team2_score
    team2.points_against -= current_pmatch.team1_score

    if current_pmatch.team1_score > current_pmatch.team2_score:
        team1.wins -= 1
        team2.losses -= 1
    else:
        team1.losses -= 1
        team2.wins -= 1

    current_pmatch.winner = False
    team1.save()
    team2.save()
    current_pmatch.save()

    reportPMatch(tournament, request)

def genTournament(tournament, request):
    if len(tournament.matches.all()) == 0: #Creates matches if there are none
        no_teams = tournament.teams.all().count()
        no_matches = no_teams - 1

        for i in range(no_matches):
            match = TMatch(match_number = i + 1)
            match.save()
            tournament.matches.add(match)

        genParents(request)


        #This can be simplified immensly
        if no_matches < 4 and no_matches > 1: #We have either a 3 or 4 team bracket
            semis_matches = no_matches - 1

            for i in range(semis_matches):
                #2+1 vs 3- 1
                match = tournament.matches.get(match_number=2+i)
                match.team1 = tournament.teams.get(seed=2-i)
                match.team2 = tournament.teams.get(seed=3+i)
                match.save()

            if no_matches == 2:
                match = tournament.matches.get(match_number=1)
                match.team1 = tournament.teams.get(seed=1)

        if  no_matches < 8 and no_matches > 3: #We have between 5 and 8 teams
            quarters_matches = no_matches - 3

            for i in range(quarters_matches): #Fills in the matches in the quarters div
                match=tournament.matches.get(match_number=4+i)
                match.team1 = tournament.teams.get(seed=4-i)
                match.team2 = tournament.teams.get(seed=5+i)
                match.save()

            semis_teams_to_fill = 4 - quarters_matches;
            matches_to_fill = 2;

            if semis_teams_to_fill - matches_to_fill >= 0:
                for i in range(semis_teams_to_fill-matches_to_fill): #number of matches to fill with 2 teams
                    match=tournament.matches.get(match_number=2+i)
                    match.team1 = tournament.teams.get(seed=3+i)
                    match.team2 = tournament.teams.get(seed=2-i)
                    match.save()

                #then add singles if possible???
                for i in range(semis_teams_to_fill - (semis_teams_to_fill - matches_to_fill) * 2): #Calculates the number of single teams to fill
                    match=tournament.matches.get(match_number=3-i)
                    match.team1 = tournament.teams.get(seed=1+i)
                    match.save()

            #or just add singles, there are no doubles
            if semis_teams_to_fill <= 2:
                for i in range(semis_teams_to_fill):
                    match=tournament.matches.get(match_number=3-i) #fill match 3 first, which corresponds to seed #1
                    match.team1 = tournament.teams.get(seed=1+i)
                    match.save()

        if  no_matches < 16 and no_matches > 7: #We have between 16 and 9 teams
            sixteen_matches = no_matches - 7

            for i in range(sixteen_matches): #Fills in the matches in the quarters div
                match=tournament.matches.get(match_number=8+i)
                match.team1 = tournament.teams.get(seed=8-i)
                match.team2 = tournament.teams.get(seed=9+i)
                match.save()

            quarters_teams_to_fill = 8 - sixteen_matches;
            matches_to_fill = 4;

            if quarters_teams_to_fill - matches_to_fill >= 0:
                for i in range(quarters_teams_to_fill-matches_to_fill): #number of matches to fill with 2 teams
                    match=tournament.matches.get(match_number=4+i)
                    match.team1 = tournament.teams.get(seed=5+i)
                    match.team2 = tournament.teams.get(seed=4-i)
                    match.save()

                #then add singles if possible???
                for i in range(quarters_teams_to_fill - (quarters_teams_to_fill - matches_to_fill) * 2): #Calculates the number of single teams to fill
                    match=tournament.matches.get(match_number=7-i)
                    match.team1 = tournament.teams.get(seed=1+i)
                    match.save()

            #or just add singles, there are no doubles
            if quarters_teams_to_fill <= 4:
                for i in range(quarters_teams_to_fill):
                    match=tournament.matches.get(match_number=7-i) #fill match 3 first, which corresponds to seed #1
                    match.team1 = tournament.teams.get(seed=1+i)
                    match.save()

        if  no_matches < 32 and no_matches > 15: #We have between 32 and 17 teams
            thirtytwo_matches = no_matches - 15

            for i in range(thirtytwo_matches): #Fills in the matches in the quarters div
                match=tournament.matches.get(match_number=16+i)
                match.team1 = tournament.teams.get(seed=16-i)
                match.team2 = tournament.teams.get(seed=17+i)
                match.save()

            sixteen_teams_to_fill = 16 - thirtytwo_matches;
            matches_to_fill = 8;

            if sixteen_teams_to_fill - matches_to_fill >= 0:
                for i in range(sixteen_teams_to_fill-matches_to_fill): #number of matches to fill with 2 teams
                    match=tournament.matches.get(match_number=8+i)
                    match.team1 = tournament.teams.get(seed=9+i)
                    match.team2 = tournament.teams.get(seed=8-i)
                    match.save()

                #then add singles if possible???
                for i in range(sixteen_teams_to_fill - (sixteen_teams_to_fill - matches_to_fill) * 2): #Calculates the number of single teams to fill
                    match=tournament.matches.get(match_number=15-i)
                    match.team1 = tournament.teams.get(seed=1+i)
                    match.save()

            #or just add singles, there are no doubles
            if sixteen_teams_to_fill <= 8:
                for i in range(semis_teams_to_fill):
                    match=tournament.matches.get(match_number=15-i) #fill match 3 first, which corresponds to seed #1
                    match.team1 = tournament.teams.get(seed=1+i)
                    match.save()

def reportTMatch(tournament, request):
    if int(request.POST["match"]) == 1: #Final match, don't need to lead into another match
        current_match = tournament.matches.get(match_number = 1)
        current_match.team1_score = request.POST["score1"]
        current_match.team2_score = request.POST["score2"]
        current_match.winner = True
        current_match.save()
    else:
        current_match = tournament.matches.get(match_number = int(request.POST["match"]))
        next_match = tournament.matches.get(match_number = current_match.parent_match)
        current_match.team1_score = request.POST["score1"]
        current_match.team2_score = request.POST["score2"]
        current_match.winner = True

        if current_match.parent_game == 1: #If we put the winner into slot 1
            if request.POST["score1"] > request.POST["score2"]: #If team 1 wins
                next_match.team1 = current_match.team1
            else: #if team 2 wins
                next_match.team1 = current_match.team2
        elif current_match.parent_game == 2: #If we put winner into slot 2
            if request.POST["score1"] > request.POST["score2"]: #If team 1 wins
                next_match.team2 = current_match.team1
            else: #if team 2 wins
                next_match.team2 = current_match.team2

        next_match.save()
        current_match.save()

def addteam(request):

    tournament = Tournament.objects.all().last()

    try:
        tournament.teams.get(team_name=request.POST["team_name"])

    except: #If the team doesn't exist yet
        team = TTeam(team_name=request.POST["team_name"], teammate1=request.POST["teammate1"], teammate2=request.POST["teammate2"],
        teammate1_phone=request.POST["phone1"], teammate2_phone=request.POST["phone2"], seed=0, payment=tournament.payment_options.get(option = request.POST["payment"]))
        team.save()
        tournament.teams.add(team)

def checkHeadToHead(tournament, team1, team2):
    team1wins = 0
    team2wins = 0


    try:
        pool = tournament.pools.filter(team1.pool_set)
        if team2 in pool: #Both teams were in the same pool
            #get the matches with these 2 teams and record their head to head win/loss
            try:
                match = pool.matches.get(team1 = team1, team2 = team2)
                if match.team1_score > match.team2_score:
                    team1wins += 1
                else:
                    team2wins += 1
            except:
                print("no matches with " + team1.team_name + " as team1 and " + team2.team_name + " as team2")

            try:
                matches = pool.matches.get(team1 = team2, team2 = team1)
                if match.team1_score > match.team2_score:
                    team2wins += 1
                else:
                    team1wins += 1
            except:
                print("no matches with " + team1.team_name + " as team1 and " + team2.team_name + " as team2")

            if team1wins > team2wins:
                return True
            else:
                return False
        else:
            return False
    except:
        return False

def genSeeding(tournament):

    teams = tournament.teams.all()
    for i in range(len(teams)):
        team = teams[i]
        team.seed = i+1
        team.save()

    team_losses = -1
    team_pd = -1
    for i in range(len(teams)):
        if teams[i].losses == team_losses and teams[i].point_differential == team_pd: #We have a tie
            print('found a tie')
            if checkHeadToHead(tournament, teams[i], teams[i-1]): #If the first team has a better head to head
                teams[i].seed -= 1
                teams[i-1].seed += 1
                teams[i].save()
                teams[i-1].save()
        team_losses = teams[i].losses
        team_pd = teams[i].point_differential

def genPoolsMatches(pool):
    no_rounds = pool.teams.count() - 1

    for i in range(no_rounds): #Create the correct number of rounds
        round = PRound(round_number = i + 1)
        round.save()
        pool.rounds.add(round)

    teams = pool.teams.all()
    no_teams = pool.teams.count()

    team_order=list(range(0, int(math.ceil(no_teams/2)))) #creates a list that we will rotate to determine games
    for i in range(int(math.floor(no_teams/2))):
        team_order.append(no_teams-1-i)

    dummy_team = -1
    if(len(team_order) % 2 == 1): #Odd numbered teams
        dummy_team = len(team_order) #When this team is matched, we have a bye
        team_order.insert(int(math.ceil(no_teams/2)), dummy_team)
        print(dummy_team)


    matches_per_round = int(len(team_order)/2)
    for i in range(no_rounds): #Adds appropriate matches for each round
        round = pool.rounds.get(round_number = i+1) #Get correct round
        for j in range(matches_per_round): #adds 2 teams to a round
            team1 = j
            team2 = matches_per_round + j


            if team_order[team1] != dummy_team and team_order[team2] != dummy_team: #Real game
                pmatch = PMatch(team1 = teams[team_order[team1]], team2 = teams[team_order[team2]], match_number=i*matches_per_round + j)
                pmatch.save()
                round.matches.add(pmatch)
                print(pmatch)

        print(team_order)
        shuffled_team = team_order.pop(int(len(team_order)/2)) #Rotates the teams so there are no conflicting matches in the next round
        team_order.insert(1, shuffled_team)
        shuffled_team = team_order.pop(int(len(team_order)/2))
        team_order.append(shuffled_team)

def genParents(request): #not proud of this one
    tournament = Tournament.objects.all().last()
    for i in range(tournament.matches.all().count()):
        match = tournament.matches.get(match_number=i+1)
        if match.match_number == 1:
            match.parent_match = 0
            match.parent_game = 0
        elif match.match_number == 2:
            match.parent_match = 1
            match.parent_game = 2
        elif match.match_number == 3:
            match.parent_match = 1
            match.parent_game = 1
        elif match.match_number == 4:
            match.parent_match = 3
            match.parent_game = 2
        elif match.match_number == 5:
            match.parent_match = 2
            match.parent_game = 2
        elif match.match_number == 6:
            match.parent_match = 2
            match.parent_game = 1
        elif match.match_number == 7:
            match.parent_match = 3
            match.parent_game = 1
        elif match.match_number == 8:
            match.parent_match = 7
            match.parent_game = 2
        elif match.match_number == 9:
            match.parent_match = 6
            match.parent_game = 2
        elif match.match_number == 10:
            match.parent_match = 5
            match.parent_game = 2
        elif match.match_number == 11:
            match.parent_match = 4
            match.parent_game = 2
        elif match.match_number == 12:
            match.parent_match = 4
            match.parent_game = 1
        elif match.match_number == 13:
            match.parent_match = 5
            match.parent_game = 1
        elif match.match_number == 14:
            match.parent_match = 6
            match.parent_game = 1
        elif match.match_number == 15:
            match.parent_match = 7
            match.parent_game = 1
        elif match.match_number == 16:
            match.parent_match = 15
            match.parent_game = 2
        elif match.match_number == 17:
            match.parent_match = 14
            match.parent_game = 2
        elif match.match_number == 18:
            match.parent_match = 13
            match.parent_game = 2
        elif match.match_number == 19:
            match.parent_match = 12
            match.parent_game = 2
        elif match.match_number == 20:
            match.parent_match = 11
            match.parent_game = 1
        elif match.match_number == 21:
            match.parent_match = 10
            match.parent_game = 1
        elif match.match_number == 22:
            match.parent_match = 9
            match.parent_game = 1
        elif match.match_number == 23:
            match.parent_match = 8
            match.parent_game = 1
        elif match.match_number == 24:
            match.parent_match = 8
            match.parent_game = 2
        elif match.match_number == 25:
            match.parent_match = 9
            match.parent_game = 2
        elif match.match_number == 26:
            match.parent_match = 10
            match.parent_game = 2
        elif match.match_number == 27:
            match.parent_match = 11
            match.parent_game = 2
        elif match.match_number == 28:
            match.parent_match = 12
            match.parent_game = 1
        elif match.match_number == 29:
            match.parent_match = 13
            match.parent_game = 1
        elif match.match_number == 30:
            match.parent_match = 14
            match.parent_game = 1
        elif match.match_number == 31:
            match.parent_match = 15
            match.parent_game = 1
        match.save()
