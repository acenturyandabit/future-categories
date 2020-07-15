f=open("scraped-axios.json",errors="replace")
lines=f.readlines()
clean=[i.replace(u'\ufffd', '') for i in lines]
clean=[i.replace('\\n', '') for i in clean]
o=open("clean-axios.json","w")
o.writelines(clean)