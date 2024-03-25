
import pandas as pd
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.agents import tools, Tool
from langchain_openai import OpenAI
#from chat2plot import chat2plot
from lida import Manager, TextGenerationConfig , llm  
import base64
import base64
from io import BytesIO
from PIL import Image               # to load images
from IPython.display import display # to display images
import os
from dotenv import load_dotenv
_ = load_dotenv()
llm = OpenAI(openai_api_key= os.environ['OPENAI_API_KEY'])

def get_ggsheet(url):
    sheet_url = url.split('edit')[0]+"export?format=csv"
    return sheet_url

class Analyst:
    def __init__(self, data_path, llm, file_type=None):
        self.df_path = data_path
        
        if file_type is None:
            self.file_type= data_path.split('.')[-1]
            
        self.llm = llm
        if isinstance(llm, (ChatOpenAI, OpenAI)):
            self.provider = 'openai'
        self.prompt = None
        
        
    def _read2df(self,path, csv=True):
        if csv:
            df = pd.read_csv(path)
            return df
        else:
            df = pd.read_excel(path, engine='openpyxl')
            return df
    def _display_plot(self, fig):
        fig_data = base64.b64decode(fig.raster)
        image = Image.open(BytesIO(fig_data))
        display(image)

    def package_plot(self,img):
        if isinstance(img, bytes):
            return img
        else:
            buffer = BytesIO()
            img.save(buffer, format="JPEG")  # You can specify the desired image format here (e.g., PNG)
            # Get the bytes data from the buffer
            image_bytes = buffer.getvalue()
            # Encode the bytes data to base64
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
            return image_base64

    def _build_pandas_agent(self, llm, df):
        
        agent = create_pandas_dataframe_agent(llm, df, verbose=True)
        return agent
    
    def _build_plot_agents(self, df):
        provider = self.provider
        from lida import Manager, TextGenerationConfig , llm  
        from chat2plot import chat2plot
        textgen_config = TextGenerationConfig(n=1, temperature=0, use_cache=False)
        lida = Manager(text_gen = llm(provider)) # palm, cohere ..
        summary = lida.summarize(df, textgen_config=textgen_config)

        c2p = chat2plot(df)
        return lida, summary, c2p
    def classify(self,prompt):
        model = self.llm
        base = """
        Analyze the following user input and determine if it is requesting a plot of a story, data, or any other form of graphical representation.

        If the input explicitly asks for a plot, description of a plot, or any graphical representation, respond with "PLOT REQUESTED".
        If the input does not ask for a plot or graphical representation, respond with "NO PLOT REQUESTED".

        User Input: "{}"
        """

        #model = ChatOpenAI(model_name="gpt-3.5-turbo-16k-0613")
        res = model.invoke(base.format(prompt))
        # Checking for the specific responses
        if res.strip() == "PLOT REQUESTED":
            return True
        else:
            return False

    def run_plotting(self,query):
        
        goals = self.plot_agent.goals(self.summary, n=1, persona= query) # generate goals
        charts = self.plot_agent.visualize(summary=self.summary, goal=goals[0]) 
        if charts:
            self._display_plot(charts[0])
            #return goals[0].rationale
            response = {'text':goals[0].rationale, 'plot':charts[0].raster}
        else:

            from chat2plot import chat2plot
            try:
                result = self.c2p(query)
                result.figure.show()  
                #return result.explanation 
                plot_code = self.package_plot(result.figure)
                explanation = result.explanation 
                response = {'text':explanation, 'plot':plot_code}
            except Exception as e:
                print(str(e))
                return "Agent ecountered error while try to generate plot. Make sure the fields you want to plot exist in dataframe"
        return response
    
    def initialize(self):
        from dotenv import load_dotenv
        _ = load_dotenv()

        def run_analysis(query):
            res = self.analyst.run(query)
            return res

        
        if self.df_path.endswith('csv'):
            csv = True
        else:
            csv = False
        
        self.df = self._read2df(self.df_path, csv=csv)
        self.analyst =self._build_pandas_agent(self.llm, self.df)
        #self.plot_agent, self.summary, self.c2p = self._build_plot_agents(self.df)
        return self
    
    def run(self, query):
        #return {'text':"The asset with the highest price is BTC-USD with a current price of 17897.426.", 'plot':''}
        cls = self.classify(query)
        if cls:
            response = self.run_plotting(query)
            return response
        else:
            agent = self.analyst
            res = agent.invoke({'input':query})['output']

            return {'text':res, 'plot':None}


def get_file_infomation(df):
    ncols = df.shape[1]
    nrows = df.shape[0]
    columns = list(df.columns)
    return {'ncols':ncols, 'nrows':nrows, 'columns':columns}
