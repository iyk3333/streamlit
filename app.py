import streamlit as st
import streamlit.components.v1 as components
from network import *
from util import *
from flask import Flask, render_template
from jinja2 import Environment, PackageLoader, select_autoescape


st.set_page_config(layout="wide")

latitude = 127
longtitude = 64

def settings():
    st.title("설정")

    question1 = st.radio("▶ 추천 받고 싶은 개수를 선택하세요.", ["10", "20"])
    # question2 = st.radio("▶ 추천 받고 싶은 개수를 선택하세요.", ["10", "20"])


def recommendations():
    st.title("추천")


    # key = "594B1FE4-401F-333F-9CA4-53D7A89E6673"
    # url = "http://map.vworld.kr/js/vworldMapInit.js.do?version=2.0&apiKey={key}".format(key=key)



    components.html(
        '''
            <!-- https://www.vworld.kr/dev/v4dv_icbsource_s002.do?pageIndex=1&brdIde=SRC_0000000000000007&searchCondition=0&searchKeyword= -->

            <!doctype html>
            <html lang="en">
              <head>
                <meta charset="utf-8">
                <meta http-equiv="X-UA-Compatible" content="chrome=1">
                <meta name="viewport" content="initial-scale=1.0, user-scalable=no, width=device-width">
                <style type="text/css">
                body,iframe {
                  width: 100%;
                  height: 100%;
                  position: relative;
                  overflow: auto;
                }
                #map {
                  width: 100%;
                  height: 400px;
                }
                #result {
                    width: 100%;
                    height: 400px;
                    margin-top: 50px;
                }
                </style>
                <title>장소 추천 지도</title>
              </head>
              <body>
      
                <div>
                    <input type="text"  id="searchValue" name="query" value="" style="width: 200px;
                    height:30px; padding=10px; margin-bottom:20px; margin-right:10px; margin-top: 30px" />
                    <input type="button" onclick="search(37.524159333019, 126.87287978897)" style="width:40px;height:30px; margin-top: 30px;" value="추천"/>
                </div>
           
                <div id="map" ></div>

                <div id="result" >
                    <h3>정보</h3>
                </div>


                <script type="text/javascript" src="http://map.vworld.kr/js/vworldMapInit.js.do?version=2.0&apiKey=594B1FE4-401F-333F-9CA4-53D7A89E6673"></script>
                <script src="https://code.jquery.com/jquery-2.2.3.min.js"></script>
                <script type="text/javascript">
                    vw.ol3.MapOptions = {
                        basemapType : vw.ol3.BasemapType.GRAPHIC,
                        controlDensity : vw.ol3.DensityType.BASIC,
                        interactionDensity : vw.ol3.DensityType.FULL,
                        controlsAutoArrange : true,
                        homePosition : vw.ol3.CameraPosition,
                        initPosition : vw.ol3.CameraPosition,
                    };
                    map = new vw.ol3.Map("map", vw.ol3.MapOptions);

                    var features = new Array();
                    var styleCache = new Array();
                    var search = function(a,b){
                        $.ajax({
                            type: "get",
                            url: "http://127.0.0.1:8000",
                            data : {latitude: a, longitude: b},
                            dataType: 'json',
                            async: true,
                            timeout: 30000,
                            success: function(data) {
                                alert(data)
                                //alert("success");
  
                            },
                            error: function(XMLHttpRequest, textStatus, errorThrown){
                                alert("code: "+XMLHttpRequest.status+textStatus+errorThrown);
                            }
                        });
                        
                    }

                   function convertCoordinates(lon, lat) {
                        var x = (lon * 20037508.34) / 180;
                        var y = Math.log(Math.tan(((90 + lat) * Math.PI) / 360)) / (Math.PI / 180);
                        y = (y * 20037508.34) / 180;
                        return [x, y];
                   }


                    var move = function(x,y){//127.10153, 37.402566
                        map.getView().setCenter(convertCoordinates(x,y)); // 지도 이동
                        map.getView().setZoom(17);
                    }

                    var prev = new Array();
                    var overlayElement
                    /* 클릭 이벤트 제어 */
                    map.on("click", function(evt) {

                        for(var i=0;i< prev.length;i++){
                            map.removeOverlay(prev[i]);
                        }
                        //prev = new Array();


                        var coordinate = evt.coordinate //좌표정보
                        var pixel = evt.pixel
                        var cluster_features = [];
                        var features = [];

                         // map.deleteOverlay(overlayInfo);
                        //선택한 픽셀정보로  feature 체크
                        map.forEachFeatureAtPixel(pixel, function(feature, layer) {
                            var title = feature.get("title");
                            var road = feature.get("road");
                            var parcel = feature.get("parcel");
                            var category = feature.get("category");
                            var point = feature.get("point");
                            if(title.length>0){

                                var overlayElement= document.createElement("div"); // 오버레이 팝업설정

                                overlayElement.setAttribute("class", "overlayElement");
                                overlayElement.setAttribute("style", "background-color: #F399CC; border: 2px solid white; color:white");
                                overlayElement.setAttribute("onclick", "deleteOverlay('"+feature.get("id")+"')");
                                overlayElement.innerHTML="<p>"+title+"</p>";

                                document.getElementById("result").innerHTML = 
                                    "<h3>"+
                                    "placeName: " + title + "<br>"+
                                    "address: " + parcel + road + "<br>"+
                                    "category: " + category + "<br>"+
                                    "point: (" + point.x + ", " + point.y + ")"+
                                    " </h3>";

                                var overlayInfo = new ol.Overlay({
                                    id:feature.get("id"),
                                    element:overlayElement,
                                    offset: [0, -70], // 정보의 위치
                                    position: ol.proj.transform([feature.get("point").x*1, feature.get("point").y*1],'EPSG:4326', "EPSG:900913")
                                });

                                if(feature.get("id") != null){
                                    map.removeOverlay(map.getOverlayById(feature.get("id")));
                                }
                                prev.push(overlayInfo);
                                map.addOverlay(overlayInfo);
                            }
                        });
                    });

                    /**
                        오버레이 삭제
                    */
                    var deleteOverlay = function(id){
                        map.removeOverlay(map.getOverlayById(id));
                    }

                </script>
              </body>
            </html>

        ''',
        height=2000
    )




    # location = Payload().locationInfo
    #
    # # 37.524159333019, 126.87287978897
    # location['latitude'] = 37.524159333019
    # location['longitude'] = 126.87287978897
    #
    # page_icon = "⬇"
    # buttonResult = st.button("추천⬇")
    # #
    # #
    # #
    # if buttonResult:



def main():
    st.sidebar.header("메뉴")

    page = st.sidebar.radio("메뉴를 선택하세요.", ["설정", "추천"])


    if page == "설정":
        settings()
    elif page == "추천":
        recommendations()


main()