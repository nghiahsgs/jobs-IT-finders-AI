from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from src.rag.document_loader import JobDocumentLoader
from src.rag.sql_agent import SQLAgent
from src.utils.logger import get_logger

logger = get_logger(__name__)

class RAGService:
    def __init__(self):
        # Khởi tạo các components
        self.loader = JobDocumentLoader()
        self.embeddings = OpenAIEmbeddings()
        self.chat_history = []  # Thêm chat history
        self.setup_vector_store()
        self.setup_retriever()
        self.setup_chain()
        
        # Thêm SQL Agent
        self.sql_agent = SQLAgent()

    def setup_vector_store(self):
        """Khởi tạo và setup vector store"""
        try:
            # Load documents từ database
            documents = self.loader.load_documents()
            
            # Khởi tạo vector store
            self.vector_store = Chroma(
                collection_name="job_collection",
                embedding_function=self.embeddings,
                persist_directory="./chroma_db"
            )
            
            # Add documents vào vector store
            self.vector_store.add_documents(documents)
            
        except Exception as e:
            logger.error(f"Error setting up vector store: {str(e)}")
            raise

    def setup_retriever(self):
        """Khởi tạo retriever"""
        try:
            self.retriever = self.vector_store.as_retriever(
                search_type="mmr",  # Sử dụng MMR để đa dạng hóa kết quả
                search_kwargs={
                    "k": 5,
                    "fetch_k": 10,
                    "lambda_mult": 0.7
                }
            )
        except Exception as e:
            logger.error(f"Error setting up retriever: {str(e)}")
            raise

    def setup_chain(self):
        """Khởi tạo chain"""
        try:
            llm = ChatOpenAI(
                temperature=0,
                model="gpt-4-turbo-preview"
            )
            
            template = """Trả lời câu hỏi dựa trên context sau:

            {context}

            Câu hỏi: {question}

            Hướng dẫn:
            - Trả lời bằng tiếng Việt
            - Nếu là câu hỏi về số lượng/thống kê, hãy trả lời chính xác con số
            - Nếu không tìm thấy thông tin trong context, trả lời "Tôi không tìm thấy thông tin về câu hỏi của bạn trong dữ liệu hiện có."
            - Format câu trả lời rõ ràng, dễ đọc
            """
            
            prompt = ChatPromptTemplate.from_template(template)
            
            self.chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=self.retriever,
                combine_docs_chain_kwargs={"prompt": prompt},
                return_source_documents=True,  # Thêm option này
                memory=None  # Tắt memory để không cần chat history
            )
            
        except Exception as e:
            logger.error(f"Error setting up chain: {str(e)}")
            raise

    def query(self, question: str) -> str:
        """
        Quyết định sử dụng RAG hay SQL Agent dựa vào loại câu hỏi
        """
        try:
            if self._is_statistical_question(question):
                # Sử dụng SQL Agent cho câu hỏi thống kê
                return self.sql_agent.query(question)
            else:
                # Sử dụng RAG cho câu hỏi thông thường
                result = self.chain.invoke({
                    "question": question,
                    "chat_history": self.chat_history
                })
                
                # Lưu chat history nếu cần
                self.chat_history.append((question, result["answer"]))
                
                return result["answer"]
                
        except Exception as e:
            logger.error(f"Error processing question: {str(e)}")
            return "Xin lỗi, đã có lỗi xảy ra khi xử lý câu hỏi của bạn."

    def _is_statistical_question(self, question: str) -> bool:
        """
        Kiểm tra xem có phải câu hỏi thống kê không
        """
        statistical_keywords = [
            "bao nhiêu", "số lượng", "tổng", "total",
            "count", "đếm", "thống kê", "có mấy",
            "tìm", "liệt kê", "danh sách"
        ]
        return any(keyword in question.lower() for keyword in statistical_keywords)

    def refresh_knowledge(self):
        """
        Refresh vector store với dữ liệu mới từ database
        """
        try:
            documents = self.loader.load_documents()
            self.vector_store.delete_collection()
            self.vector_store = Chroma(
                collection_name="job_collection",
                embedding_function=self.embeddings,
                persist_directory="./chroma_db"
            )
            self.vector_store.add_documents(documents)
            logger.info("Knowledge base refreshed successfully")
        except Exception as e:
            logger.error(f"Error refreshing knowledge base: {str(e)}")
            raise