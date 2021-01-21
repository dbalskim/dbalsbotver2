import discord
import random
import requests
from bs4 import BeautifulSoup

client = discord.Client()

emogilist = ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟')

@client.event
async def on_ready():
    print(client.user.id)
    print("ready")
    game = discord.Game("/도움말")
    await client.change_presence(status=discord.Status.online, activity=game)


@client.event
async def on_message(message):
    if (message.content.startswith("하이 드발스") or message.content.startswith("하이드발스")):
        await message.channel.send("네")



    if message.content.startswith("/투표"):
        message_split = message.content.split()

        if ((len(message_split)) > 3 and (len(message_split)) <= 12):
            embed = discord.Embed(title="**[:loudspeaker:투표] " + message_split[1] + "**", description=":small_orange_diamond:아래에서 원하시는 항목을 투표해주세요", color=0x1ca54d)
            vote = message_split[2:]

            for i in range(len(vote)):
                embed.add_field(name=emogilist[i], value=vote[i], inline=False)

            message = await message.channel.send(embed=embed)

            for i in range(len(vote)):
                await message.add_reaction(emogilist[i])

        elif ((len(message_split)) > 12):
            embed = discord.Embed(title="드발스봇", description=":warning:투표 기능은 10개 항목까지만 지원합니다. 각 항목은 띄어쓰기 없이 작성해 주세요.", color=0x1ca54d)
            embed.add_field(name="사용법", value="/투표 투표주제 항목1 항목2 ⋯")
            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="드발스봇", description=":warning:투표 항목은 2개 이상부터 가능합니다.", color=0x1ca54d)
            embed.add_field(name=":small_orange_diamond:사용법", value="/투표 투표주제 항목1 항목2 ⋯")
            await message.channel.send(embed=embed)




    if message.content.startswith("/팀 뽑기 "):
        blueEmbed = discord.Embed(title="블루팀", description="블루팀 멤버", color=0x3c7ed9) #블루팀 embed생성
        redEmbed = discord.Embed(title="레드팀", description="레드팀 멤버", color=0xe44530) #레드팀 embed생성
        blueMembers = 0 #블루팀 인원수 체크용
        redMembers = 0 #레드팀 인원수 체크용

        message_split = message.content.split() #띄어쓰기를 기준으로 문자열 쪼개기
        members = message_split[2:] #이름만 가져오기 위해 2번째 인덱스부터 추출

        for member in members: #멤버 수 만큼 반복
            if(blueMembers >= int(len(members) // 2)): #블루팀 인원이 과반수 이상이라면 해당 멤버를 레드팀에 추가
                redEmbed.add_field(name="레드팀", value=member, inline=True)
                redMembers += 1 #레드팀에 한 명이 추가됐다고 기록

            elif(redMembers >= int(len(members) // 2)): #레드팀 인원이 과반수 이상이라면 해당 멤버를 블루팀에 추가
                blueEmbed.add_field(name="블루팀", value=member, inline=True)
                blueMembers += 1 #블루팀에 한 명이 추가됐다고 기록

            else: #만일 모두 아니라면
                team = random.randint(1, 3) #랜덤 함수를 통해 1 또는 2의 난수를 획득

                if(team == 1): #만일 1이면 블루팀에 추가
                    blueEmbed.add_field(name="블루팀", value=member, inline=True)
                    blueMembers += 1 #블루팀에 한 명이 추가됐다고 기록

                else: #아니라면 (2라면) 레드팀에 추가
                    redEmbed.add_field(name="레드팀", value=member, inline=True)
                    redMembers += 1 #레드팀에 한 명이 추가됐다고 기록

        await message.channel.send(embed=blueEmbed) #출력
        await message.channel.send(embed=redEmbed)



    if message.content.startswith("/실검"):
        embed = discord.Embed(title="드발스봇", description="네이버 실검 1 ~ 10위입니다", color=0x1ca54d)
        embed.set_thumbnail(url="https://t1.daumcdn.net/cfile/tistory/99E493445C0D20A143")
        json = requests.get("https://www.naver.com/srchrank?frm=main").json()
        ranks = json.get("data")
        i = 1
        for r in ranks:
            if i >= 11:
                break
            else:
                keyword = r.get("keyword")
                embed.add_field(name=str(i)+"위", value=keyword, inline=False)
                i += 1
        await message.channel.send(embed=embed)


    if message.content.startswith("/전적"):
        try:
            tierImage = {'Unrank':'//opgg-static.akamaized.net/images/medals/default.png', 'Bronze':'//opgg-static.akamaized.net/images/medals/bronze_4.png?image=q_auto:best&v=1',
                             'Silver':'//opgg-static.akamaized.net/images/medals/silver_2.png?image=q_auto:best&v=1', 'Gold':'//opgg-static.akamaized.net/images/medals/gold_2.png?image=q_auto:best&v=1',
                             'pPlatinum':'//opgg-static.akamaized.net/images/medals/platinum_2.png?image=q_auto:best&v=1', 'Diamond':'//opgg-static.akamaized.net/images/medals/diamond_1.png?image=q_auto:best&v=1',
                             'Master':'//opgg-static.akamaized.net/images/medals/master_1.png?image=q_auto:best&v=1', 'Grandmaster':'//opgg-static.akamaized.net/images/medals/grandmaster_1.png?image=q_auto:best&v=1',
                             'Challenger':'//opgg-static.akamaized.net/images/medals/challenger_1.png?image=q_auto:best&v=1'}
            tiers = ('Unrank', 'Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Master', 'Grandmaster', 'Challenger')
            message_split = message.content.split()
            name = ''.join(message_split[1:])
            embed = discord.Embed(title="드발스봇", description="다음은 " + name + "님의 op.gg 검색 결과입니다.", color=0x1ca54d)

            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
            url = 'https://www.op.gg/summoner/userName=' + name

            res = requests.get(url, headers = headers)

            soup = BeautifulSoup(res.content, 'html.parser')

            soloRank = str(soup.select('div.TierRank'))
            if 'Unranked' in soloRank:
                embed.add_field(name="솔랭:dagger:", value=soloRank[32:-7], inline=False)
            else:
                embed.add_field(name="솔랭:dagger:", value=soloRank[23:-7], inline=False)
            for t in tiers:
                if t in soloRank:
                    embed.set_thumbnail(url="https:" + tierImage[t])

            freeRank = str(soup.select('div.sub-tier__rank-tier '))
            if 'Unranked' in freeRank:
                embed.add_field(name="자랭:crossed_swords:", value=freeRank[43:-7], inline=False)
            else:
                embed.add_field(name="자랭:crossed_swords:", value=freeRank[35:-7], inline=False)

            mostChamp = str(soup.select('div.ChampionName')[0].text)
            embed.add_field(name="가장 많이 플레이한 챔피언", value=mostChamp, inline=True)
            games = str(soup.select('div.Title')[0].text)

            embed.add_field(name="횟수", value=games[0:-7] + " games", inline=True)

            winRate = str(soup.select('div.WinRatioGraph')[-1].text)
            embed.add_field(name="승률", value=winRate, inline=False)

            
            

            embed.add_field(name="자세한 정보는 op.gg에서 확인하세요", value='https://www.op.gg/summoner/userName=' + name, inline=False)


            await message.channel.send(embed=embed)

        except:
            embed = discord.Embed(title="드발스봇", description=":warning:해당 소환사의 전적이 존재하지 않습니다.", color=0x1ca54d)
            embed.add_field(name=":small_orange_diamond:사용법", value="/전적 소환사닉네임")
            await message.channel.send(embed=embed)



    if message.content.startswith("/날씨"):
        try:
            message_split = message.content.split()
            if(len(message_split) == 1):
                loc = "부평"
            else:
                loc = str(message_split[1:])[2:-2]

            embed = discord.Embed(title="드발스봇", description="다음은 " + loc + "의 날씨입니다:sunrise_over_mountains:", color=0x1ca54d)

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
            url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=' + loc + "날씨"

            res = requests.get(url, headers=headers)

            soup = BeautifulSoup(res.content, 'html.parser')

            todaytemp = str(soup.select('span.todaytemp')[0].text) + "℃"
            cast = str(soup.select('p.cast_txt')[0].text)


            embed.add_field(name=todaytemp + ":thermometer:", value=cast, inline=False)

            sensible = str(soup.select('span.num')[2].text)

            embed.add_field(name="체감 온도", value=sensible, inline=False)

            await message.channel.send(embed=embed)

        except:
            embed = discord.Embed(title="드발스봇", description=":warning:해당 지역의 날씨 정보가 존재하지 않습니다.", color=0x1ca54d)
            embed.add_field(name=":small_orange_diamond:사용법", value="/날씨 [지역]")
            await message.channel.send(embed=embed)


    if message.content.startswith("/코로나"):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%BD%94%EB%A1%9C%EB%82%98'
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')

        embed = discord.Embed(title="드발스봇", description="국내 코로나 현황입니다:microbe:", color=0x1ca54d)

        patients = str(soup.select('p.info_num')[0].text)
        inspection = str(soup.select('p.info_num')[1].text)
        Quarantine = str(soup.select('p.info_num')[2].text)
        dead = str(soup.select('p.info_num')[3].text)
        domesticNewPatients = str(soup.select('em.info_num')[0].text)
        overseasNewPatients = str(soup.select('em.info_num')[1].text)

        newPatients = int(domesticNewPatients) + int(overseasNewPatients)


        embed.add_field(name="확진환자", value=patients, inline=True)
        embed.add_field(name="검사 중", value=inspection, inline=True)
        embed.add_field(name="격리 해제", value=Quarantine, inline=True)
        embed.add_field(name="사망자", value=dead, inline=True)
        embed.add_field(name="신규 확진자", value=newPatients, inline=True)

        await message.channel.send(embed=embed)



        





    if message.content.startswith("/도움말"):
        embed = discord.Embed(title="드발스봇", description=":small_orange_diamond:드발스봇을 이용해주셔서 감사합니다", color=0x1ca54d)
        embed.add_field(name=":small_blue_diamond:호출", value="하이 드발스", inline=False)
        embed.add_field(name=":small_blue_diamond:투표", value="/투표 투표주제 항목1 항목2 ⋯", inline=False)
        embed.add_field(name=":small_blue_diamond:네이버 실시간 검색어 확인", value="/실검", inline=False)
        embed.add_field(name=":small_blue_diamond:롤 전적 검색", value="/전적 소환사닉네임", inline=False)
        embed.add_field(name=":small_blue_diamond:날씨 확인", value="/날씨 [지역]", inline=False)
        embed.add_field(name=":small_blue_diamond:코로나 현황 확인", value="/코로나", inline=False)

        
        await message.channel.send(embed=embed)





client.run("ODAxNzM4OTE5NjEwODEwMzY5.YAlDjg.RRU39J29SEyniIvwHSiBOgltwHE")