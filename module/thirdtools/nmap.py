import nmap3
from conf.log import logger
nmap = nmap3.Nmap()

def run_nmap(network,ports="",np=False):
    if np:
        # args="-sV -sC -Pn -p-"
        args=f"-sV -sC  -p{ports}"
        logger.info(f"RUN COMMAND:nmap -sV -sC  -p{ports} {network}")
        results = nmap.nmap_subnet_scan(network,args)
    else:
        args = f"-sV -sC -Pn -p{ports}"
        logger.info(f"RUN COMMAND:nmap -sV -sC -Pn -p{ports} {network}")
        results = nmap.nmap_subnet_scan(network, args)
    tmp_result=[]
    for ip,result in results.items():
        if ip=="stats" or ip=="runtime":
            continue
        for port in result["ports"]:
            if port["state"]=="open":
                portid=port["portid"]
                service=port["service"]["name"]
                tmp_result.append({"ip":ip,"port":portid,"service":service})
                if service=="http" or service=="https":
                    print(f"{service}://{ip}:{portid}")
                else:
                    print({"ip":ip,"port":portid,"service":service})
    return tmp_result

