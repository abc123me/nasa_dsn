from net.auth import CredentialManager, generatePasswordHash

to = 5

cm = CredentialManager()
for i in range(0, to):
	print("user [" + str(i) + "]: " + str(cm.tryAddCredentials("user" + str(i), generatePasswordHash("user" + str(i)), i)))
cm.saveCredentialsJSON("creds.json")
hsh = cm.getHash("user0")
slt = cm.getSalt("user0")
print("" + str(hsh))
print("" + str(slt))

cmn = CredentialManager()
cmn.loadCredentialsJSON("creds.json")
for i in range(0, to):
	hsh = cm.getHash("user" + str(i))
	slt = cm.getSalt("user" + str(i))
	hshn = cmn.getHash("user" + str(i))
	sltn = cmn.getSalt("user" + str(i))
	print("" + str(hshn))
	print("" + str(sltn))
	print(hsh == hshn)
	print(slt == sltn)