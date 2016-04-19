import urllib2;
from lxml import etree;
from bs4 import BeautifulSoup;
from Writer import Writer;
from sets import Set;


########################################################################
class Parser:
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.base = "http://www.icd10data.com";
        self.writer = Writer("temp.txt");
        self.direction = Set(["right","left"]);
        self.areas = Set(["joint","shoulder","elbow","vertebra"]);
        
    #----------------------------------------------------------------------
    def getmainlist(self):
        """"""
        response = urllib2.urlopen("http://www.icd10data.com/ICD10CM/Codes/M00-M99");
        self.htmlparser = etree.HTMLParser()
        tree = etree.parse(response, self.htmlparser);  
        self.hreflist = tree.xpath("/html/body/div[2]/div/div[4]/ul/li/a/@href");
        self.hreflist = self.hreflist;
        self.getsublist(self.hreflist);
        self.writer.close();
    
    #----------------------------------------------------------------------
    def getsublist(self,hreflist):
        """"""
        for href in hreflist:
            response = urllib2.urlopen(self.base+href);
            soup = BeautifulSoup(response.read(),"lxml");
            lists = soup.select("ul li span a");
            for l in lists:
                self.selectcode(l.attrs["href"]);
            
    #----------------------------------------------------------------------
    def selectcode(self,link):
        """"""
        response = urllib2.urlopen(self.base+link);
        soup = BeautifulSoup(response.read().decode("gbk").encode("utf-8"),"html.parser");
        greenimgs = soup.select('img[src="/images/bullet_triangle_green.png"]');
        for greenimg in greenimgs:
            sibilings = greenimg.parent.findChildren("span");
            code = sibilings[0].a.text;
            description = self.setdescription(sibilings[1],sibilings[0].a);
            sets = description.split(",");
            side = "NULL";
            area = "NULL";
            area,side = self.setarea_side(sets);
            self.writer.insert(code, description, 10, side, area, 0);

    #----------------------------------------------------------------------
    def setdescription(self,description_obj,link_obj):
        """"""
        if (description_obj.text.find(u"\u2026\u2026")!=-1):
            response = urllib2.urlopen(self.base+link_obj.attrs["href"]);
            soup = BeautifulSoup(response.read().decode("gbk").encode("utf-8"),"html.parser");
            description = soup.select("div div div h2")[0].text;
            return description;
        return description_obj.text;
    
    #----------------------------------------------------------------------
    def setarea_side(self,desc_sets):
        """"""
        area = "NULL";
        side = "NULL";
        if (len(desc_sets)>1):
            area =  desc_sets[-1].strip().lower();
            specificarea = area;
            if (specificarea.startswith("left")):
                side = "left";
                area = specificarea.replace("left","").strip();
            elif (specificarea.startswith("right")):
                side = "right";
                area = specificarea.replace("right","").strip();
            elif (specificarea.startswith("unspecified") and (specificarea!="unspecified area")):
                area = specificarea.replace("unspecified", "").strip();
            if len(area)==0:
                area = "NULL";  
            if (area!="NULL" and area not in self.areas):
                self.areas.add(area);
        elif (len(desc_sets)==1):
            for direction in self.direction:
                if (desc_sets[0].find(direction)!=-1):
                    side = direction;
                    break;
            for pos in self.areas:
                if (desc_sets[0].find(pos)!=-1):
                    area = pos;
                    break;
        if (area=="joint" and side=="NULL"):
            area = "NULL"
        return area, side;

    
if __name__=="__main__":
    parser = Parser();
    #print parser.setarea_side(["Staphylococcal arthritis", "left shoulder"]);
    #print parser.setarea_side(["Staphylococcal arthritis, left shoulder"]);
    #print parser.setarea_side(["Direct infection of right shoulder in infectious and parasitic diseases classified elsewhere"]);
    
    parser.getmainlist();
    
    