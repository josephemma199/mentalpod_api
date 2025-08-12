import os, json
from openai import AsyncOpenAI
class ChatLLM:
    def __init__(self):
        self.model=os.getenv('OPENAI_MODEL','gpt-4o-mini'); self.key=os.getenv('OPENAI_API_KEY'); self.client=AsyncOpenAI(api_key=self.key) if self.key else None
    async def complete(self,system,user):
        if not self.client: return '{"youtube_titles":["Sample Title"],"sections":[{"heading":"Intro","bullets":["Hook","Context"]}]}'
        r=await self.client.chat.completions.create(model=self.model,messages=[{"role":"system","content":system},{"role":"user","content":user}],temperature=0.7)
        return r.choices[0].message.content
    def _j(self,t):
        import json
        try:return json.loads(t)
        except: return None
    def safe_parse_topic_ideas(self,t,default_count=12):
        j=self._j(t); 
        if j is None:
            lines=[l.strip('- ').strip() for l in t.splitlines() if l.strip()];
            return [{"title":l,"rationale":"N/A","seo_keywords":[],"angle_tags":[]} for l in lines[:default_count]]
        return [{"title":i.get('title',''),"rationale":i.get('rationale',''),"seo_keywords":i.get('seo_keywords',[]),"angle_tags":i.get('angle_tags',[])} for i in j]
    def safe_parse_outline(self,t):
        j=self._j(t); 
        if j is None:
            secs=[]; cur={"heading":"Section","bullets":[]}
            for line in t.splitlines():
                if line.startswith('#'):
                    if cur['bullets']: secs.append(cur)
                    cur={"heading":line.strip('# ').strip(),"bullets":[]}
                elif line.startswith('- '): cur['bullets'].append(line[2:].strip())
            if cur['bullets']: secs.append(cur)
            return {"youtube_titles":["Draft Title"],"sections":secs}
        return j
    def safe_parse_hostdoc(self,t,role):
        j=self._j(t); 
        if j is None:
            return type('HostDocObj',(object,),{"role":role,"tone_notes":["Warm, curious, collaborative"],"perspective_prompts":["Open with a vignette."],"must_cover":["Define terms; one practical tool"],"caution_flags":["Avoid overgeneralizing"]})()
        return type('HostDocObj',(object,),{"role":role, **j})()
    def safe_parse_analysis(self,t,fallback_title=None):
        j=self._j(t); 
        if j is None:
            return type('Analysis',(object,),{"title":fallback_title,"summary":t[:400],"highlights":[],"takeaways":[]})()
        return type('Analysis',(object,),{"title":j.get('title',fallback_title),"summary":j.get('summary',''),"highlights":j.get('highlights',[]),"takeaways":j.get('takeaways',[])})()
