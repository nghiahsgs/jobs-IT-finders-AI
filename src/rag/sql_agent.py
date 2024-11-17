import os
from langchain_community.utilities import SQLDatabase
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI

class SQLAgent:
    def __init__(self):
        # Kết nối database
        self.db = SQLDatabase.from_uri(
            os.getenv("DATABASE_URL"),
            sample_rows_in_table_info=3
        )
        
        # Khởi tạo LLM
        self.llm = ChatOpenAI(
            temperature=0,
            model="gpt-4-turbo-preview"
        )
        
        # Tạo toolkit và agent
        self.toolkit = SQLDatabaseToolkit(
            db=self.db,
            llm=self.llm
        )
        
        self.agent = create_sql_agent(
            llm=self.llm,
            toolkit=self.toolkit,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            verbose=True,
            handle_parsing_errors=True
        )

    def query(self, question: str) -> str:
        """
        Chuyển câu hỏi thành SQL query và thực thi
        """
        try:
            # Thêm context về schema
            enhanced_prompt = f"""
            Bạn là một SQL expert. Hãy trả lời câu hỏi sau bằng tiếng Việt, 
            sử dụng dữ liệu từ bảng 'job' với các cột:
            - job_title: tiêu đề công việc
            - company_name: tên công ty
            - status: trạng thái ('Open' hoặc 'Close')
            - company_industry: ngành nghề
            - job_description: mô tả công việc
            
            Câu hỏi: {question}
            """
            
            result = self.agent.run(enhanced_prompt)
            return result
            
        except Exception as e:
            # logger.error(f"Error executing SQL query: {str(e)}")
            return "Xin lỗi, đã có lỗi xảy ra khi truy vấn database."