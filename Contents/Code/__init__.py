NAME    = L('Title')
PREFIX   = '/video/IndianTVChannels'

ART      = 'art-default.jpg'
ICON     = 'icon-desitv.png'

IndianTVChannels = 'Indian TV Channels'
IndianTVChannelsURL = 'http://www.desirulzs.net/'
IndianTVChannelsTHUMB = 'icon-IndianTVChannels.png'
DESITVFORUM = 'Desi TV Forum'
DESITVFORUMURL = 'http://'

http = 'http:'

RE_LIST_ID = Regex('listId: "(.+?)", pagesConfig: ')
RE_CONTENT_ID = Regex('CONTENT_ID = "(.+?)";')

STARPLUS = 'Star Plus'
ZEETV = 'Zee Tv'
SONYTV = 'Sony Tv'
LIFEOK = 'Life OK'
SAHARAONE = 'Sahara One'
STARJALSHA = 'Star Jalsha'
COLORS = 'Colors Channel'
SABTV = 'Sab TV'
STARPRAVAH = 'Star Pravah'
MTV = 'MTV (India/Pakistan)'
CHANNELV = 'Channel [V]'
BINDASSTV = 'Bindass TV'
UTVSTARS = 'UTV Stars'
NEWS = 'News Channels'

filter = [STARPLUS, ZEETV, SONYTV, LIFEOK, SAHARAONE, STARJALSHA, COLORS, SABTV, STARPRAVAH, MTV, CHANNELV, BINDASSTV, UTVSTARS]

def Start():
  ObjectContainer.title1 = NAME
  ObjectContainer.art = R(ART)

  DirectoryObject.thumb = R(ICON)
  DirectoryObject.art = R(ART)
  EpisodeObject.thumb = R(ICON)
  EpisodeObject.art = R(ART)
  VideoClipObject.thumb = R(ICON)
  VideoClipObject.art = R(ART)

@handler(PREFIX, NAME, art=ART, thumb=ICON)
def MainMenu():
  oc = ObjectContainer()
  oc.add(DirectoryObject(key=Callback(IndianTVChannelsChannels, url=IndianTVChannelsURL), title=IndianTVChannels, thumb=R(IndianTVChannelsTHUMB)))

  return oc

@route(PREFIX + '/IndianTVChannelschannels')
def IndianTVChannelsChannels(url):
  oc = ObjectContainer(title2=IndianTVChannels)

  html = HTML.ElementFromURL(url)

  for item in html.xpath("//li[@id='cat41']//div[@class='foruminfo td']"):
    try:
      # Channel title
      channel = item.xpath("./div/div/div/h2/a/text()")[0]
      
      # Channel link
      link = item.xpath("./div/div/div/h2/a/@href")[0]
      if link.startswith("http") == False:
        link = IndianTVChannelsURL + link
    except:
      continue

    try:
      # If the specified image URL is relative, then translate it
      image = item.xpath("./img[@class='forumicon']")[0].get('src')
      if image.startswith("http") == False:
        image = IndianTVChannelsURL + image
    except:
      continue

    #Log ('channel: ' + channel)
    #Log ('img src: ' + image)

    # Add the found item to the collection
    #Log ('channel: ' + channel)

    if channel in filter:
      oc.add(DirectoryObject(key=Callback(IndianTVChannelsShowsMenu, url=link, title=channel), title=channel, thumb=image))
    
  # If there are no channels, warn the user
  if len(oc) == 0:
    return ObjectContainer(header=IndianTVChannels, message="ErrorNoChannel")

  return oc

####################################################################################################

@route(PREFIX + '/IndianTVChannelsshowsmenu')
def IndianTVChannelsShowsMenu(url, title):
  oc = ObjectContainer(title2=title)

  html = HTML.ElementFromURL(url)
  
  for item in html.xpath("//div[@class='forumbitBody']//div[@class='foruminfo']"):
    try:
      # Show title
      show = item.xpath("./div/div/div/h2/a/text()")[0]
      
      # Show link
      link = item.xpath("./div/div/div/h2/a/@href")[0]
      if link.startswith("http") == False:
        link = IndianTVChannelsURL + link
    except:
      continue

    # Add the found item to the collection
    oc.add(DirectoryObject(key=Callback(IndianTVChannelsEpisodesMenu, url=link, title=show), title=show))
    
  # If there are no channels, warn the user
  if len(oc) == 0:
    return ObjectContainer(header=title, message="ErrorNoShow")

  return oc

####################################################################################################

@route(PREFIX + '/IndianTVChannelsepisodesmenu')
def IndianTVChannelsEpisodesMenu(url, title):
  oc = ObjectContainer(title2=title)

  html = HTML.ElementFromURL(url)
  
  for item in html.xpath("//ol[@id='stickies']//h3[@class='threadtitle']"):
    try:
      # Episode title
      episode = item.xpath("./a/text()")[0]
      
      # episode link
      link = item.xpath("./a/@href")[0]
      if link.startswith("http") == False:
        link = IndianTVChannelsURL + link
    except:
      continue

    # Add the found item to the collection
    oc.add(DirectoryObject(key=Callback(IndianTVChannelsEpisodeLinksMenu, url=link, title=episode), title=episode))
    
  # If there are no channels, warn the user
  if len(oc) == 0:
    return ObjectContainer(header=title, message="ErrorNoEpisodes")

  return oc

####################################################################################################
import urlparse
@route(PREFIX + '/IndianTVChannelsepisodelinksmenu')
def IndianTVChannelsEpisodeLinksMenu(url, title):
  oc = ObjectContainer(title2=title)

  html = HTML.ElementFromURL(url)
  
  items = getDailymotion(html)
  
  for item in items:
    try:
      # Video site
      videosite = item.xpath("./text()")[0]

      # Video link
      link = item.xpath("./@href")[0]
      link = quickLinksURL(link)
    except:
      continue
    
    # Add the found item to the collection
    if link.find('dailymotion') != -1:
      Log ('dailymotion link: ' + link)
      oc.add(VideoClipObject(
        url = link, 
        title = videosite, 
        thumb = Resource.ContentsOfURLWithFallback(R(ICON), fallback=R(ICON))))
    
    # If there are no channels, warn the user
  if len(oc) == 0:
    return ObjectContainer(header=title, message="ErrorNoEpisodeLinks")

  return oc
  
####################################################################################################

def quickLinksURL(url):
  if url.find('.tv') != -1:
    domain = urlparse.urlparse(url)[1]
    path = urlparse.urlparse(url)[2] + '?' + urlparse.urlparse(url)[3] + urlparse.urlparse(url)[4] + urlparse.urlparse(url)[5]
    url = 'http://' + domain.replace(domain,"www.quicklinks.tv") + path

    html = HTML.ElementFromURL(url)
    url = html.xpath("//iframe/@src")[0]

    return url

####################################################################################################

def getDailymotion(html):
  items = html.xpath("//div[@class='content']//b[contains(font/text(),'Dailymotion 720p')]/following-sibling::a[count(. | //b[count(//b[contains(font/text(),'Dailymotion 720p')]/preceding-sibling::b)+2]/preceding-sibling::a) = count(//b[count(//b[contains(font/text(),'Dailymotion 720p')]/preceding-sibling::b)+2]/preceding-sibling::a)]")
  return items

####################################################################################################

@route(PREFIX + '/testmenu')
def TestMenu(url, title):
  return ObjectContainer(header="Empty", message="Unable to display videos for this show right now.")

####################################################################################################
