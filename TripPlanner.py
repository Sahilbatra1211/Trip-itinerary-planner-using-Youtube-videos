# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 01:29:23 2023

@author: sahilbatra
"""
import os
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain import OpenAI, SerpAPIWrapper, LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import AzureOpenAI
from googleapiclient.discovery import build
from langchain.document_loaders import YoutubeLoader
import requests
from langchain.chains import LLMChain

from dotenv import load_dotenv
load_dotenv()
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def getYoutubeVideos(query: str):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    api_key = "AIzaSyDATvNLM9fSJHYe1jwdXp3mff98R9Nm-e4"
    
    youtube = build(
        'youtube',
        'v3',
        developerKey=api_key
        )

    request = youtube.search().list(
        part="snippet",
        channelType="any",
        maxResults=5,
        order="relevance",
        q="iternary to goa trip with budget",
        type="video"
    )
    
    response = request.execute()
    return response
  
def getTranscriptOfVideo(videoId):
    print(videoId)
    url = f'https://www.youtube.com/watch?v=RGKIAx97k7k'
    print(url)
    loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
    documents= loader.load()   
    lang= "English"
    url2=  f'http://video.google.com/timedtext?lang={lang}&v={videoId}'
    data=requests.get(url2)
    return documents
    
def createIternaryFromVideos(res):
    prompt = PromptTemplate(
        input_variables=["context"],
        template="You are an AI assistant that creates an iteranry from the given {context}")
    
    llm = AzureOpenAI(deployment_name="OpenAiWhatsAppChat", 
                      temperature=0.9, 
                      max_tokens=800,
                      top_p=0.5,
                      frequency_penalty=0,
                      presence_penalty=0,
                      best_of=1)
    
    context = getTranscriptOfVideo(res["items"][1]['id']['videoId'])
    prompt = PromptTemplate(
        input_variables=["context"],
        template="You are an AI bot that creates iternary for amritsar for 4 days with 5000 budget and refer to your knowledge and given contetext to create perfect iteranary. Context: {context}")
    print(context)
    chain = LLMChain(llm=llm, prompt=prompt)
    print(chain.run(context))
  
def main():
    res= getYoutubeVideos("trip to himachal")
    print(res)
    createIternaryFromVideos(res)
