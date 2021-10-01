from django.shortcuts import render
from django.core.exceptions import ValidationError
from .models import League, Match, Team, TMatch, Bracket, Week
from . forms import LeagueScoreReport
from django.http import Http404, JsonResponse
from django.contrib.auth import authenticate, login
import math

# Create your views here.
def leaguesignup(request):

    league = League.objects.all().last()

    if request.method == "POST":

        try:
            league.teams.get(team_name=request.POST["team_name"])
        except: #Team hasn't been added yet
            team = Team(team_name=request.POST["team_name"], teammate1=request.POST["teammate1"], teammate2=request.POST["teammate2"],
            teammate1_phone=request.POST["phone1"], teammate2_phone=request.POST["phone2"])
            team.save()
            league.teams.add(team)

    return render(request, 'league/leaguesignup.html', {'league':league})

def schedule(request, league_id = League.objects.all().last().pk):
    league = League.objects.get(pk=league_id)

    if request.method == "POST":

        if 'enable-editing' in request.POST:
            username, password = request.POST["username"], request.POST["password"]
            user = authenticate(username=username, password=password)
            try:
                login(request, user)
            except:
                message = "Not the correct login. Please contact your tournament organizer to get access to score editing."
                return render(request, 'tournament/tournamentbracket.html', {'tournament':tournament, "message":message})

        if "generate-matches" in request.POST and request.POST["password"] == league.password: #add the matches
            if league.matches.count() == 0:
                genMatches(request)

        if "report-score" in request.POST: #reporting a league score

            reportLScore(league, request)

        if "tmatch-id" in request.POST:

            if (int(request.POST["score1"]) >= 2 or int(request.POST["score2"]) >= 2):
                reportTScore(league, request)
            else: #Note a valid score
                message = "Not a valid score. One team must have at least 2 wins"
                return render(request, 'league/schedule.html', {'league':league, "message":message})


        if "generate-brackets" in request.POST and request.POST["password"] == league.password:
            if league.brackets.count() == 0:
                genBrackets(league, request)

    return render(request, 'league/schedule.html', {'league':league})

def previousleagues(request):
    all_leagues = League.objects.all()
    return render(request, 'league/previousleagues.html', {'all_leagues':all_leagues})

#Stolen from internet, don't know how it works
def seed( n ):
    """ returns list of n in standard tournament seed order

    Note that n need not be a power of 2 - 'byes' are returned as zero
    """

    ol = [1]

    for i in range( math.ceil( math.log(n) / math.log(2) ) ):

        l = 2*len(ol) + 1

        ol = [e if e <= n else 0 for s in [[el, l-el] for el in ol] for e in s]

    return ol

def reportLeagueScore(request):
    league = League.objects.get(pk = int(request.GET["league-id"]))
    reportLScore(league, request)

    return JsonResponse({'success':"successfully reported score"})

def updateLeagueScore(request): #subtracts all previous values and then reports score normally
    league = League.objects.get(pk = int(request.GET["league-id"]))

    match = league.matches.get(pk = int(request.GET["match-id"]))

    game = int(request.GET["game-no"])

    origscore1 = 0
    origscore2 = 0
    if game == 1:
        origscore1 = match.game1_team1_score
        origscore2 = match.game1_team2_score
        match.winner1 = False
    elif game == 2:
        origscore1 = match.game2_team1_score
        origscore2 = match.game2_team2_score
        match.winner2 = False
    elif game == 3:
        origscore1 = match.game3_team1_score
        origscore2 = match.game3_team2_score
        match.winner3 = False

    match.save()

    team1 = match.team1
    team2 = match.team2

    team1.points_for -= origscore1
    team1.points_against -= origscore2
    team2.points_for -= origscore2
    team2.points_against -= origscore1

    if origscore1 > origscore2:
        team1.wins -= 1
        team2.losses -= 1
    else:
        team1.losses -= 1
        team2.wins -= 1

    team1.save()
    team2.save()

    reportLScore(league, request)


    return JsonResponse({'success':"successfully updated score"})


def reportLScore(league, request):


    match = league.matches.get(pk=request.GET["match-id"])
    if int(request.GET["game-no"]) == 1:
        if match.winner1 == False:
            match.game1_team1_score = int(request.GET["score1"])
            match.game1_team2_score = int(request.GET["score2"])
            match.winner1 = True
            match.save()

            team1 = league.teams.get(team_name = match.team1.team_name)
            team2 = league.teams.get(team_name = match.team2.team_name)

            team1.points_for += match.game1_team1_score
            team1.points_against += match.game1_team2_score
            team2.points_for += match.game1_team2_score
            team2.points_against += match.game1_team1_score
            team1.point_differential = team1.points_for - team1.points_against
            team2.point_differential = team2.points_for - team2.points_against

            if match.game1_team1_score > match.game1_team2_score:
                team1.wins += 1
                team2.losses += 1
            else:
                team1.losses += 1
                team2.wins += 1

            team1.save()
            team2.save()
    if int(request.GET["game-no"]) == 2:
        if match.winner2 == False:
            match.game2_team1_score = int(request.GET["score1"])
            match.game2_team2_score = int(request.GET["score2"])
            match.winner2 = True
            match.save()

            team1 = league.teams.get(team_name = match.team1.team_name)
            team2 = league.teams.get(team_name = match.team2.team_name)

            team1.points_for += match.game2_team1_score
            team1.points_against += match.game2_team2_score
            team2.points_for += match.game2_team2_score
            team2.points_against += match.game2_team1_score
            team1.point_differential = team1.points_for - team1.points_against
            team2.point_differential = team2.points_for - team2.points_against

            if match.game2_team1_score > match.game2_team2_score:
                team1.wins += 1
                team2.losses += 1
            else:
                team1.losses += 1
                team2.wins += 1

            team1.save()
            team2.save()
    if int(request.GET["game-no"]) == 3:

        if match.winner3 == False:
            match.game3_team1_score = int(request.GET["score1"])
            match.game3_team2_score = int(request.GET["score2"])
            match.winner3 = True
            match.save()

            team1 = league.teams.get(team_name = match.team1.team_name)
            team2 = league.teams.get(team_name = match.team2.team_name)

            team1.points_for += match.game3_team1_score
            team1.points_against += match.game3_team2_score
            team2.points_for += match.game3_team2_score
            team2.points_against += match.game3_team1_score
            team1.point_differential = team1.points_for - team1.points_against
            team2.point_differential = team2.points_for - team2.points_against

            if match.game3_team1_score > match.game3_team2_score:
                team1.wins += 1
                team2.losses += 1
            else:
                team1.losses += 1
                team2.wins += 1

            team1.save()
            team2.save()

    #Check if week can be completed
    week_matches = league.matches.filter(week_number = match.week_number)
    week_complete = True
    for match in week_matches:
        if match.winner1 and match.winner2 and match.winner3:
            continue
        else:
            week_complete = False
            break
    if week_complete:
        week = league.weeks.get(week_number = match.week_number)
        week.completed = True
        week.save()

        #Check to see if all weeks are completed
        weeks = league.weeks.all()
        all_weeks_complete = True
        for week in weeks:
            if week.completed:
                continue
            else:
                all_weeks_complete = False
                break
        if all_weeks_complete:
            league.weeks_completed = True
            league.save()


#TODO: could be simplified
def reportTScore(league, request):
    bracket = league.brackets.get(id=request.POST["bracket-id"])
    match = bracket.matches.get(id=request.POST["tmatch-id"])


    match.winner=True
    match.team1_score = request.POST["score1"]
    match.team2_score = request.POST["score2"]
    match.save()

    if match.round_number != 1: #there is another match after this one
        winner_match = bracket.matches.get(round_number = match.round_number -1 , match_number = math.floor((match.match_number+1)/2))

        loser = match.team1
        #Add winner to parent match
        if match.match_number % 2 == 1:
            if request.POST["score1"] > request.POST["score2"]:
                winner_match.team1 = match.team1
                loser=match.team2
            else:
                winner_match.team1 = match.team2
                loser=match.team1
        else:
            if request.POST["score1"] > request.POST["score2"]:
                winner_match.team2 = match.team1
                loser=match.team2
            else:
                winner_match.team2 = match.team2
                loser=match.team1
        winner_match.save()


        #Add loser to correct consolation match
        if bracket.sub_bracket_num == 1:
            try:
                consolation_bracket = league.brackets.get(bracket_num = bracket.bracket_num, sub_bracket_num = match.round_number)
                consolation_match = consolation_bracket.matches.get(round_number = match.round_number-1, match_number = math.floor((match.match_number+1)/2))
                if match.match_number % 2 == 1:
                    consolation_match.team1 = loser
                else:
                    consolation_match.team2 = match.team2
                consolation_match.save()
            except:
                print("no consolation bracket here")

            #If they go into a bye, move to the next match
            if consolation_match.team1.team_name == "Bye" or consolation_match.team2.team_name =="Bye":
                next_match = consolation_bracket.matches.get(round_number = consolation_match.round_number - 1, match_number = math.floor((consolation_match.match_number+1)/2))
                if consolation_match.match_number % 2 == 1:
                    next_match.team1 = loser
                else:
                    next_match.team2 = loser
                next_match.save()

def genTMatches(bracket, no_rounds):
    for i in range(no_rounds):
        for j in range(2**(no_rounds - i - 1)):
            match = TMatch(round_number=no_rounds-i, match_number=j+1)
            match.save()
            bracket.matches.add(match)

def checkHeadToHead(league, team1, team2):

    team1wins = 0
    team2wins = 0

    #get the matches with these 2 teams and record their head to head win/loss
    try:
        matches = league.matches.filter(team1 = team1, team2 = team2)
        for i in range(len(matches)):
            if matches[i].game1_team1_score > matches[i].game1_team2_score:
                team1wins += 1
            else:
                team2wins += 1
            if matches[i].game2_team1_score > matches[i].game2_team2_score:
                team1wins += 1
            else:
                team2wins += 1
            if matches[i].game3_team1_score > matches[i].game3_team2_score:
                team1wins += 1
            else:
                team2wins += 1
    except:
        print("no matches with " + team1.team_name + " as team1 and " + team2.team_name + " as team2")

    try:
        matches = league.matches.filter(team1 = team2, team2 = team1)
        for i in range(len(matches)):
            if matches[i].game1_team1_score > matches[i].game1_team2_score:
                team2wins += 1
            else:
                team1wins += 1
            if matches[i].game2_team1_score > matches[i].game2_team2_score:
                team2wins += 1
            else:
                team1wins += 1
            if matches[i].game3_team1_score > matches[i].game3_team2_score:
                team2wins += 1
            else:
                team1wins += 1
    except:
        print("no matches with " + team1.team_name + " as team1 and " + team2.team_name + " as team2")

    if team1wins > team2wins:
        return True
    else:
        return False


def genSeeding(league):

    teams = league.teams.all()
    for i in range(len(teams)):
        team = teams[i]
        team.seed = i+1
        team.save()

    #Check for ties and if we can do a head to head tie breaker
    team_losses = -1
    team_pd = -1
    for i in range(len(teams)):
        if teams[i].losses == team_losses and teams[i].point_differential == team_pd: #We have a tie
            print('found a tie')
            if checkHeadToHead(league, teams[i], teams[i-1]): #If the first team has a better head to head
                teams[i].seed -= 1
                teams[i-1].seed += 1
                teams[i].save()
                teams[i-1].save()
        team_losses = teams[i].losses
        team_pd = teams[i].point_differential

def genBrackets(league, request):

    genSeeding(league)

    teams = league.teams.all().order_by('seed')
    teams_added = 0

    bye_team = Team.objects.get(team_name="Bye")
    #Adding teams to correct brackets
    for i in range(int(request.POST["num-brackets"])):
        bracket = Bracket(bracket_num = i+1, sub_bracket_num=i+1) #Main bracket
        bracket.save()
        league.brackets.add(bracket)
        for j in range(int(request.POST["teams" + str(i + 1)])): #loops based on given number
            bracket.teams.add(teams[teams_added])
            bracket.save()
            teams_added += 1

        #generate consolation Brackets
        #TODO:shorten this
        no_teams = bracket.teams.count()
        if no_teams > 3 and no_teams < 6:
            for j in range(1):
                bracket = Bracket(bracket_num = i+1, sub_bracket_num = j + 2)
                bracket.save()
                #gen matches/
                genTMatches(bracket, j+1)
                league.brackets.add(bracket)
        if no_teams > 5 and no_teams < 10:
            for j in range(2):
                bracket = Bracket(bracket_num = i+1, sub_bracket_num = j + 2)
                bracket.save()
                genTMatches(bracket, j+1)
                league.brackets.add(bracket)
        if no_teams > 9 and no_teams < 17:
            for j in range(3):
                bracket = Bracket(bracket_num = i+1, sub_bracket_num = j + 2)
                bracket.save()
                genTMatches(bracket, j+1)
                league.brackets.add(bracket)

        #Generating the matches
        #TODO: shorten this
        no_rounds = 0;
        order=[]
        if no_teams > 0 and no_teams < 3:
            no_rounds = 1;
        elif no_teams > 2 and no_teams < 5:
            no_rounds = 2;
        elif no_teams > 4 and no_teams < 9:
            no_rounds = 3;
        elif no_teams > 8 and no_teams < 17:
            no_rounds = 4;


        #gets main bracket and generates the matches for it
        bracket = league.brackets.get(bracket_num = i + 1, sub_bracket_num = 1)
        genTMatches(bracket, no_rounds)

        #Populating matches with correct teams
        bracket_teams = bracket.teams.all().order_by('seed')
        no_teams = bracket_teams.count()
        order=seed(no_teams)
        matches = bracket.matches.order_by("-round_number", "match_number")
        for j in range(2**(no_rounds-1)):
            match = matches.get(round_number=no_rounds, match_number = j +1)
            # print(j, no_rounds, order, bracket.teams.all(), match)
            if order[2*j+1] != 0: #2 teams in this match
                match.team1 = bracket_teams[order[2*j] - 1]
                match.team2 = bracket_teams[order[2*j+1] -1]
                match.save()
            elif order[2*j+1] == 0: #The team here gets a bye
                match.team1 = bracket_teams[order[2*j] - 1]
                match.team2 = bye_team
                match.save()
                #If there's a bye here, then there's probably a corresponding bye in the consolation bracket
                if no_teams !=3 and no_teams !=5 and no_teams != 9: #In all these cases, a corresponding consolation bracket doesn't exist (There'd only be 1 team)
                    consolation_bracket = league.brackets.get(bracket_num=bracket.bracket_num, sub_bracket_num=no_rounds)
                    consolation_match = consolation_bracket.matches.get(round_number = match.round_number -1, match_number = math.floor((match.match_number + 1)/2)) #Gets the correct match to add a bye to
                    if match.match_number % 2 == 1:
                        consolation_match.team1 = bye_team
                    elif match.match_number % 2 == 0:
                        consolation_match.team2 = bye_team
                    consolation_match.save()
                #Might need to call a function to record this score

                parent = math.floor((match.match_number+1)/2)
                parent_match = matches.get(round_number=no_rounds-1, match_number=parent)
                if match.match_number % 2 == 1:
                    parent_match.team1 = bracket_teams[order[2*j]-1]
                    parent_match.save()
                else:
                    parent_match.team2 = bracket_teams[order[2*j]-1]
                    parent_match.save()

def genMatches(request):
    league = League.objects.all().last()
    no_teams = league.teams.count()
    no_weeks = int(request.POST["num-weeks"])
    rounds_per_week = int(request.POST["rounds-per-week"])

    league.num_weeks = no_weeks
    league.rounds_per_week = rounds_per_week
    league.save()

    teams = league.teams.all()
    print(teams)

    #generate weeks
    for i in range(no_weeks):
        week = Week(week_number = i + 1);
        week.save();
        league.weeks.add(week)


    team_order=list(range(0, int(math.ceil(no_teams/2)))) #creates a list that we will rotate to determine games
    for i in range(int(math.floor(no_teams/2))):
        team_order.append(no_teams-1-i)

    dummy_team = -1
    if(len(team_order) % 2 == 1): #Odd numbered teams
        dummy_team = len(team_order) #When this team is matched, we have a bye
        team_order.insert(int(math.ceil(no_teams/2)), dummy_team)
        bye = Team.objects.get(team_name = "Bye")
        league.teams.add(bye)

    matches_per_round = int(len(team_order)/2)

    for i in range(no_weeks):
        for j in range(rounds_per_week):
            for k in range(matches_per_round):
                team1 = k
                team2 = matches_per_round + k

                match = Match(week_number = i + 1, round_number = j + 1, team1=teams[team_order[team1]], team2=teams[team_order[team2]])
                match.save()
                league.matches.add(match)

            shuffled_team = team_order.pop(int(len(team_order)/2)) #Rotates the teams so there are no conflicting matches in the next round
            team_order.insert(1, shuffled_team)
            shuffled_team = team_order.pop(int(len(team_order)/2))
            team_order.append(shuffled_team)
