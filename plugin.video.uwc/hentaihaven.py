'''
    Ultimate Whitecream
    Copyright (C) 2016 mortael

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils

#460: hentaihaven.Main()
#461: hentaihaven.List(url)
#462: hentaihaven.Playvid(url, name, download)
#463: hentaihaven.Categories(url)
#464: hentaihaven.Search(url, keyword)    


def Main():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://hentaihaven.org/pick-your-poison/',463,'','')
    utils.addDir('[COLOR hotpink]Uncensored[/COLOR]','http://hentaihaven.org/ajax.php?action=pukka_infinite_scroll&page_no=1&grid_params=infinite_scroll=on&infinite_page=2&infinite_more=true&current_page=taxonomy&front_page_cats=&inner_grid%5Buse_inner_grid%5D=on&inner_grid%5Btax%5D=post_tag&inner_grid%5Bterm_id%5D=53&inner_grid%5Bdate%5D=&search_query=&tdo_tag=uncensored&sort=date',461,'','')
    List('http://hentaihaven.org/ajax.php?action=pukka_infinite_scroll&page_no=1&grid_params=infinite_scroll=on')
    xbmcplugin.endOfDirectory(utils.addon_handle)


def List(url):
    listhtml = utils.getHtml(url, '')
    listhtml = listhtml.replace('\\','')
    match1 = re.compile('<a class="thumbnail-image" href="([^"]+)".*?data-src="([^"]+)".*?<h3>[^>]+>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, name in match1:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 462, img, '')
    try:
        page = re.compile('page_no=(\d+)', re.DOTALL | re.IGNORECASE).findall(url)[0]
        page = int(page)
        npage = page + 1
        maxpages = re.compile(r'max_num_pages":(\d+)', re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
        if int(maxpages) > page:
            nextp = url.replace("no="+str(page),"no="+str(npage))
            utils.addDir('Next Page ('+str(npage)+')', nextp,461,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


def Playvid(url, name, download):
    videopage = utils.getHtml(url)
    videourl = re.compile('class="btn btn-1 btn-1e" href="([^"]+)" target="_blank"', re.DOTALL | re.IGNORECASE).findall(videopage)[0]
    if videourl:
        utils.playvid(videourl, name, download)
    else:
        utils.notify('Oh oh','Couldn\'t find a video')


def Categories(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('/tag/([^/]+)/" cla[^>]+>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catpage, name in match:
        catpage = "http://hentaihaven.org/ajax.php?action=pukka_infinite_scroll&page_no=1&grid_params=infinite_scroll=on&infinite_page=2&infinite_more=true&current_page=taxonomy&front_page_cats=&inner_grid%5Buse_inner_grid%5D=on&inner_grid%5Btax%5D=post_tag&inner_grid%5Bterm_id%5D=53&inner_grid%5Bdate%5D=&search_query=&tdo_tag=" + catpage + "&sort=date" 
        utils.addDir(name, catpage, 461, '')    
    xbmcplugin.endOfDirectory(utils.addon_handle)

