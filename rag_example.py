from src.rag.rag_service import RAGService


def main():
    # Khởi tạo RAG service
    rag = RAGService()
    
    print("Chào mừng! Hãy nhập câu hỏi của bạn (nhấn Enter để gửi, gõ 'quit' để thoát):")
    
    while True:
        # Lấy input từ người dùng
        question = input("\nCâu hỏi của bạn: ").strip()
        
        # Kiểm tra nếu người dùng muốn thoát
        if question.lower() in ['quit', 'exit', 'q']:
            print("Tạm biệt!")
            break
            
        # Bỏ qua nếu câu hỏi trống
        if not question:
            print("Vui lòng nhập câu hỏi!")
            continue
            
        # Xử lý câu hỏi và in kết quả
        print(f"Trả lời: {rag.query(question)}")
        print("-" * 50)

if __name__ == "__main__":
    main()
    # what is open job of viettel ?
    # số lượng những job tuyển python là bao nhiêu, java là bao nhiêu ?
