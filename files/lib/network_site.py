import yaml
from pprint import pprint
from os import system
import os
from subprocess import DEVNULL, STDOUT
import time
from datetime import date
def detail_site(site,tdata):
	color=None
	color_list=[]
	for key,value in site.items():
		tdata.append('<tr>')
		tdata.append('<th>%s</th>'%key.upper())
		if 'wan#' in key:
			wan_info=[]
			wan_head=[]
			wan_head.append('<table class=a><tr>')
			wan_info.append('<tr>')
			if len(value) > 1:
				for k,v in value.items():
					wan_head.append('<th>%s</th>'%k.upper())
					# wan_info.append('<td>%s</td>'%str(v).upper())
					if k.lower() == 'ce':
						if len(v.split('/')) > 1:
							if os.name == nt:
								pingcmd = 'ping -n 2'
							else:
								pingcmd = 'ping -c 2'
							if system('%s %s'%(pingcmd,v.split('/')[0])) == 0:
								color='lightgreen'
								wan_info.append('<td style="background-color: lightgreen">'+ str(v).upper()+'</td>')
								color_list.append(color)
							else:
								color='red'
								wan_info.append('<td style="background-color: red">%s</td>'%str(v).upper())
								color_list.append(color)
					else:
						wan_info.append('<td>%s</td>'%str(v).upper())
				wan_info.append('</tr></table>')
				wan_head.append('</tr>')
				wan_data = ''.join(wan_head)
				wan_data = wan_data+''.join(wan_info)
				tdata.append('<td>%s</td>'%''.join(wan_data))
			else:
				tdata.append('<td>%s</td></tr>'%value)
		else:
			if key == 'contact':
				tdata.append('<td style="padding-left: 3%">')
				for v in value:
					tdata.append('<li>%s'%v)
				tdata.append('</td></tr>')
			else:
				tdata.append('<td>%s</td></tr>'%value)
	return (color_list,color,tdata)

def detail_circuits(site,cdata,clist,color):
	cdata.append("<tr><td><h2>%s</h2></td>"%(site['site_code']))
	clist.append(site['wan#1']['provider'])
	cdata.append("<td><table><tr><th class='left'>Provider</th><th class='left'>CE</th><th class='left'>PE</th><th class='left'>BW</th></tr><tr style='background-color: %s'><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr></table>"%(color[0],site['wan#1']['provider'],site['wan#1']['CE'],site['wan#1']['PE'],site['wan#1']['BW']))
	if len(site['wan#2'])>1:
		clist.append(site['wan#2']['provider'])
		cdata.append("<td><table><tr><th class='left'>Provider</th><th class='left'>CE</th><th class='left'>PE</th><th class='left'>BW</th></tr><tr style='background-color: %s'><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr></table>"%(color[1],site['wan#2']['provider'],site['wan#2']['CE'],site['wan#2']['PE'],site['wan#2']['BW']))
	cdata.append('</tr>')
	return cdata,clist

def get_vendor():
	with open("../files/vendor/vendor.yml") as _:
		raw_vendors = (yaml.load(_, Loader=yaml.FullLoader))
	vendors = sorted(raw_vendors, key=lambda x:x['name'])
	vdata = []
	for vendor in vendors:
		vdata.append("<tr><td><h2>%s</h2></td>"%vendor['name'])
		vdata.append('<td><table><tr>')
		for k,v in vendor.items():
			if k == 'name':
				pass
			else:
				vdata.append("<th class='left'>%s</th>"%k)
		vdata.append('</tr>')
		vdata.append('<tr>')
		for k,v in vendor.items():
			if k == 'name':
				pass
			elif k == 'urls':
				vdata.append('<td style="padding-left: 3%">')
				for url in v:
					vdata.append('<h3><li><a href="%s" target="_blank">%s</a></h3>'%(url,url))
				vdata.append('</td>')
			elif k == 'attach':
				vdata.append('<td style="padding-left: 3%">')				
				for att in v:
					vdata.append("<h3><li><a href='../files/vendor/%s' target='_blank'>%s</a></h3>"%(att,att))
				vdata.append('</td>')

			else:
				vdata.append('<td><h3>%s</h3></td>'%v)
		vdata.append('</tr>')
		vdata.append("</table></td>")
		vdata.append("</tr>")
	return vdata

def sites_contacts(sites):
	scdata = []
	scdata.append("<tr><th class='left'>Site</th><th class='left'>Contacts</th></tr>")
	for site in sites:
		scdata.append('<tr><td style="padding-left: 3%"><h2>'+site['site_code']+'</h2></td>')
		scdata.append('<td style="padding-left: 3%">')
		for c in site['contact']:
			scdata.append("<h3 class='contact'><li>%s</h3>"%c)
		scdata.append('</td></tr>')
	return (scdata)

t = time.localtime()
d = date.today()
day = d.strftime("%B %d, %Y")
start_time = time.strftime("%H:%M:%S", t)
start_time=day+"-"+start_time+' UTC +8'

os.chdir('..')
index_base=''
with open ("../files/templates/html/index_base.txt",'r+') as f:
	raw = f.read()
	index_base = raw.replace('$TIME',start_time)

with open ("../index.html",'w') as f:
	f.write(index_base)

with open ('../files/site_info/site_info.yaml') as _:
	raw_sites = (yaml.load(_, Loader=yaml.FullLoader))

sites = sorted(raw_sites, key=lambda x:x['site_code'])

with open("../files/templates/html/site_index_base.txt",'r') as f:
	html_base = f.read()

raw = []
cdata=[]
clist=[]
cdata.append('<h2><tr><th>Site</th><th>Primary Circuit</th><th>Secondary Circuit</th></tr></h2>')
for site in sites:
	thead=[]
	tdata=[]
	with open("../files/templates/html/site_base.txt",'r') as f:
		site_detail = f.read()
	with open("../files/templates/html/circuit_base.txt",'r') as f:
		circuit_detail = f.read()
	raw.append("<div><a href='sites/%s.html'>%s</a></div>"%(site['site_code'],site['site_code']))
	color_list,color,tdata = detail_site(site,tdata)
	print(color_list)
	cdata,clist=detail_circuits(site,cdata,clist,color_list)

	if color:
		raw = '\n'.join(raw).replace("<div><a href='sites/%s.html'>%s</a></div>"%(site['site_code'],site['site_code'])
			,"<div style='background-color:%s'><a href='../pages/sites/%s.html'>%s</a></div>"%(color,site['site_code'],site['site_code']))
		raw = raw.splitlines()

	site_page = site_detail.replace('$TDATA$','\n'.join(tdata))
	site_page = site_page.replace('$SITE$',site['site_code'])
	site_page = site_page.replace('$TIME', start_time)
	with open ("../pages/sites/%s.html"%site['site_code'],'w') as _:
		_.writelines(site_page)

## Write Circuit Page
circuit_page = circuit_detail.replace('$TDATA$', '\n'.join(cdata))
circuit_page = circuit_page.replace('$Total$',str(len(clist)))
circuit_page = circuit_page.replace('$TIME', start_time)
with open ("../pages/circuits_index.html",'w') as _:
	_.writelines(circuit_page)

## Write Sites page
data = '\n'.join(raw)
html_base = html_base.replace('$TOTAL$',str(len(sites)))
site_page=html_base.replace('$DATA$',data)
site_page = site_page.replace('$TIME', start_time)
with open ("../pages/sites_index.html",'w') as _:
	_.writelines(site_page)

## Write Vendor page
with open("../files/templates/html/vendor_base.txt", 'r') as f:
	vendor_detail=f.read()
vdata = get_vendor()
vendor_page = vendor_detail.replace('$TDATA$','\n'.join(vdata))
vendor_page = vendor_page.replace('$TIME', start_time)
with open ("../pages/vendor_index.html",'w') as _:
	_.writelines(vendor_page)

## Write Sites_Contacts page
with open("../files/templates/html/sc_base.txt", 'r') as f:
	sc_detail=f.read()
scdata = sites_contacts(sites)
sc_page = sc_detail.replace('$TDATA$','\n'.join(scdata))
sc_page = sc_page.replace('$TIME', start_time)
with open ("../pages/sc_index.html",'w') as _:
	_.writelines(sc_page)



