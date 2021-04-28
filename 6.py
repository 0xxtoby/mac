# coding:utf-8
'''
广播攻击
'''
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
from gmpy2 import iroot
try:
    from libnum import solve_crt
except:
    print ("no module named libnum: please use `pip install libnum` to obtain it.")
    exit(0)

m = bytes_to_long(flag)
e = 3
ns = [924506488821656685683910901697171383575761384058997452768161613244316449994435541406042874502024337501621283644549497446327156438552952982774526792356194523541927862677535193330297876054850415513120023262998063090052673978470859715791539316871,\
    88950937117255391223977435698486265468789676087383749025900580476857958577458361251855358598960638495873663408330100969812759959637583297211068274793121379054729169786199319454344007481804946263873110263761707375758247409,\
    46120424124283407631877739918717497745499448442081604908717069311339764302716539899549382470988469546914660420190473379187397425725302899111432304753418508501904277711772373006543099077921097373552317823052570252978144835744949941108416471431004677]
cs = [388825822870813587493154615238012547494666151428446904627095554917874019374474234421038941934804209410745453928513883448152675699305596595130706561989245940306390625802518940063853046813376063232724848204735684760377804361178651844505881089386,4132099145786478580573701281040504422332184017792293421890701268012883566853254627860193724809808999005233349057847375798626123207766954266507411969802654226242300965967704040276250440511648395550180630597000941240639594,43690392479478733802175619151519523453201200942800536494806512990350504964044289998495399805335942227586694852363272883331080188161308470522306485983861114557449204887644890409995598852299488628159224012730372865280540944897915435604154376354144428]

m = solve_crt(cs, ns)
assert (iroot(m, 3)[1] == True)
m = iroot(m, 3)[0]
print ("solve:")
print (long_to_bytes(m)[::-1])