d#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 17:56:39 2018

@author: chaymae
"""
def enum(filename):
    """
    argument: file name
    returns:
        numbVideo:
        numbEndPoint
        numbRequest
        numbCaches
        cachesCap
        videoSizes:list it's index represent the video and items are the sizes of videos
        latencyCaches: dictionary-->key: is  endpoints (int) / value:datacenter latency of the endpoint
        latencyDataCenter:dictionary-->key: is endpoint-cache number(str) / value:The latency the specified endpoint to the specified cache 
        request:list of tuple---> (number of requests,video number,endPoint)
    """
    fh = open(filename, "r")
    
    videoSizes=list()
    latencyCaches=dict()
    latencyDataCenter=dict()
    request=list()
    
    numbVideo,numbEndPoint,numbRequest,numbCaches,cachesCap=map(int, fh.readline().strip().split())
    
    
    videoSizes= list(map(int, fh.readline().strip().split()))
    
    for endPoint in range(numbEndPoint):
        datacenter_latency,numbConnectedCaches=map(int, fh.readline().strip().split())
        latencyDataCenter[endPoint]=int(datacenter_latency)
        
        for cache in range(numbConnectedCaches):        
            latencyCaches[str(endPoint)+"-"+str(cache)]=int(fh.readline().strip().split()[1])
    for req in range(numbRequest):
        video,endPoint,requests=map(int, fh.readline().strip().split())
        request.append((requests,video,endPoint))
    fh.close()
    
    return numbVideo,numbEndPoint,numbRequest,numbCaches,cachesCap,videoSizes,latencyCaches,latencyDataCenter,request

numbVideo,numbEndPoint,numbRequest,numbCaches,cachesCap,videoSizes,latencyCaches,latencyDataCenter,request=enum("small.in")