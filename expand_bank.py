import json

with open('questions_db.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

more_questions = [
    {
        'id': 'ext_11',
        'source': 'Bộ câu hỏi mở rộng - Trọng tâm Gmetrix',
        'domain_id': 1,
        'domain_name': 'Phương pháp và mô hình Generative AI',
        'lesson_title': 'Bài 3: Các siêu tham số của LLM',
        'type': 'matching',
        'question': '(Kéo thả / Ghép nối) Ghép mỗi siêu tham số điều khiển LLM với chức năng tương ứng của nó:',
        'left_items': [
            {'id': '1', 'text': '1. Temperature (Nhiệt độ)'},
            {'id': '2', 'text': '2. Top-P (Nucleus Sampling)'},
            {'id': '3', 'text': '3. Max Tokens'},
            {'id': '4', 'text': '4. Stop Sequences (Chuỗi dừng)'}
        ],
        'right_items': [
            {'id': 'a', 'text': 'a. Giới hạn độ dài tối đa của câu trả lời mà AI được phép tạo ra.'},
            {'id': 'b', 'text': 'b. Điều khiển mức độ ngẫu nhiên và sáng tạo của câu trả lời (thấp = ổn định, cao = đa dạng).'},
            {'id': 'c', 'text': 'c. Ký tự hoặc từ ngữ báo hiệu mô hình phải dừng sinh văn bản ngay lập tức khi gặp nó.'},
            {'id': 'd', 'text': 'd. Lựa chọn từ tiếp theo chỉ trong phạm vi nhóm các từ có tổng xác suất tích lũy đạt ngưỡng P.'}
        ],
        'answer': {'1': 'b', '2': 'd', '3': 'a', '4': 'c'},
        'explanation': 'Temperature (1-b) chỉnh ngẫu nhiên/sáng tạo; Top-P (2-d) lấy mẫu tích lũy xác suất; Max Tokens (3-a) giới hạn độ dài; Stop Sequences (4-c) ngắt sinh văn bản khi gặp ký tự quy định.'
    },
    {
        'id': 'ext_12',
        'source': 'Bộ câu hỏi mở rộng - Trọng tâm Gmetrix',
        'domain_id': 1,
        'domain_name': 'Phương pháp và mô hình Generative AI',
        'lesson_title': 'Bài 5: Phân loại công cụ AI theo phương thức',
        'type': 'matching',
        'question': '(Kéo thả / Ghép nối) Ghép mỗi công cụ AI với loại phương thức chuyển đổi cốt lõi của nó:',
        'left_items': [
            {'id': '1', 'text': '1. InVideo / Runway'},
            {'id': '2', 'text': '2. DALL-E 3 / Midjourney'},
            {'id': '3', 'text': '3. Whisper (OpenAI)'},
            {'id': '4', 'text': '4. Claude / ChatGPT'}
        ],
        'right_items': [
            {'id': 'a', 'text': 'a. Text-to-Image (Văn bản thành hình ảnh)'},
            {'id': 'b', 'text': 'b. Speech-to-Text (Âm thanh/Giọng nói thành văn bản)'},
            {'id': 'c', 'text': 'c. Text-to-Video (Văn bản hoặc ảnh thành video)'},
            {'id': 'd', 'text': 'd. Text-to-Text / Multimodal reasoning (Xử lý và sinh văn bản đa phương thức)'}
        ],
        'answer': {'1': 'c', '2': 'a', '3': 'b', '4': 'd'},
        'explanation': 'InVideo/Runway: Text-to-Video (1-c); DALL-E/Midjourney: Text-to-Image (2-a); Whisper: Speech-to-Text (3-b); Claude/ChatGPT: Text-to-Text / Chatbot đa năng (4-d).'
    },
    {
        'id': 'ext_13',
        'source': 'Bộ câu hỏi mở rộng - Trọng tâm Gmetrix',
        'domain_id': 2,
        'domain_name': 'Kỹ thuật xây dựng Prompt cơ bản',
        'lesson_title': 'Bài 9: Quy trình tạo ảnh nghệ thuật bằng Prompt',
        'type': 'ordering',
        'question': '(Sắp xếp) Sắp xếp các bước để tạo một bức ảnh chất lượng cao và kiểm soát được phong cách bằng AI tạo ảnh:',
        'items': [
            {'id': 'A', 'text': 'Thêm thông số kỹ thuật đầu ra như tỷ lệ khung hình (--ar 16:9) và tham số chất lượng.'},
            {'id': 'B', 'text': 'Mô tả chủ thể chính cùng hành động cụ thể (ví dụ: chú mèo phi hành gia đang trôi bồng bềnh).'},
            {'id': 'C', 'text': 'Bổ sung bối cảnh, ánh sáng và phong cách nghệ thuật mong muốn (ví dụ: vũ trụ cyberpunk, ánh sáng neon rực rỡ, phong cách digital art 3D).'},
            {'id': 'D', 'text': 'Xem kết quả, bổ sung Negative Prompt (ví dụ: tránh mờ, méo hình) và tinh chỉnh lặp lại.'}
        ],
        'answer': ['B', 'C', 'A', 'D'],
        'explanation': 'Quy trình tạo ảnh chuẩn: (B) Chủ thể & hành động -> (C) Bối cảnh, ánh sáng, phong cách -> (A) Tham số tỷ lệ & kỹ thuật -> (D) Đánh giá, dùng Negative Prompt để loại bỏ lỗi.'
    },
    {
        'id': 'ext_14',
        'source': 'Bộ câu hỏi mở rộng - Trọng tâm Gmetrix',
        'domain_id': 3,
        'domain_name': 'Tinh chỉnh Prompt & Đánh giá mô hình',
        'lesson_title': 'Bài 14: Biện pháp giảm thiểu ảo giác',
        'type': 'multi_choice',
        'question': 'Để giảm thiểu hiện tượng ảo giác (hallucination) khi sử dụng LLM cho các công việc đòi hỏi độ chính xác cao, người dùng nên thực hiện những biện pháp nào? (Chọn 3)',
        'required_count': 3,
        'options': {
            'A': 'Cung cấp văn bản tài liệu nguồn uy tín ngay trong prompt và yêu cầu AI chỉ trả lời dựa trên tài liệu đó.',
            'B': 'Hạ tham số nhiệt độ (temperature) xuống mức thấp (ví dụ 0 hoặc 0.2).',
            'C': 'Yêu cầu AI: "Nếu không tìm thấy thông tin trong tài liệu được cung cấp, hãy trả lời là \'Tôi không biết\', không được tự suy đoán".',
            'D': 'Tăng temperature lên mức tối đa để mô hình tự do sáng tạo câu trả lời.',
            'E': 'Sử dụng prompt càng ngắn và chung chung càng tốt để không gò bó mô hình.'
        },
        'answer': ['A', 'B', 'C'],
        'explanation': 'Ba biện pháp hữu hiệu nhất ngăn ngừa ảo giác: đính kèm tài liệu nguồn và ràng buộc phạm vi trả lời (Grounding - A), giảm temperature để mô hình giữ tính tất định (B), và dặn rõ ràng từ chối trả lời nếu thiếu dữ kiện (C).'
    },
    {
        'id': 'ext_15',
        'source': 'Bộ câu hỏi mở rộng - Trọng tâm Gmetrix',
        'domain_id': 3,
        'domain_name': 'Tinh chỉnh Prompt & Đánh giá mô hình',
        'lesson_title': 'Bài 15: Kiểm tra tính nhất quán (Consistency)',
        'type': 'true_false',
        'question': 'Về việc kiểm tra tính nhất quán của câu trả lời AI, mỗi ý sau đúng hay sai?',
        'items': [
            {'id': 'a', 'text': 'Chạy cùng một câu lệnh nhiều lần trong các phiên mới (fresh chats) giúp đánh giá mức độ ổn định của câu trả lời.'},
            {'id': 'b', 'text': 'Nếu một câu trả lời được viết với giọng điệu rất tự tin thì chắc chắn nó sẽ nhất quán ở các lần hỏi tiếp theo.'},
            {'id': 'c', 'text': 'Kỹ thuật Self-consistency (Tự nhất quán) yêu cầu AI tạo ra nhiều chuỗi suy luận khác nhau rồi chọn đáp án chiếm đa số.'},
            {'id': 'd', 'text': 'Đặt temperature = 0 sẽ giúp mô hình đưa ra câu trả lời gần như hoàn toàn nhất quán giữa các lần hỏi lặp lại.'}
        ],
        'answer': {'a': True, 'b': False, 'c': True, 'd': True},
        'explanation': 'a: Đúng (thử nghiệm lặp lại kiểm tra độ ổn định). b: Sai (giọng điệu tự tin không bảo đảm tính nhất quán hay độ chính xác). c: Đúng (Self-consistency lấy đa số kết quả từ nhiều chuỗi reasoning). d: Đúng (temperature = 0 loại bỏ hầu hết tính ngẫu nhiên).'
    },
    {
        'id': 'ext_16',
        'source': 'Bộ câu hỏi mở rộng - Trọng tâm Gmetrix',
        'domain_id': 4,
        'domain_name': 'Đạo đức, Pháp luật & Tác động xã hội',
        'lesson_title': 'Bài 19: Nguyên tắc sử dụng AI có trách nhiệm (Responsible AI)',
        'type': 'multi_choice',
        'question': 'Theo các hướng dẫn về AI có trách nhiệm (Responsible AI), những nguyên tắc nào là bắt buộc khi triển khai AI trong thực tế? (Chọn 3)',
        'required_count': 3,
        'options': {
            'A': 'Tính minh bạch (Transparency): Thông báo rõ ràng cho người dùng biết khi nào họ đang tương tác với AI hoặc khi nội dung được tạo bởi AI.',
            'B': 'Công bằng & Không phân biệt đối xử (Fairness): Giảm thiểu định kiến về giới tính, chủng tộc, tôn giáo trong kết quả đầu ra.',
            'C': 'Trách nhiệm giải trình (Accountability): Luôn có con người chịu trách nhiệm về các quyết định và kết quả do AI hỗ trợ tạo ra.',
            'D': 'Tuyệt đối không cho phép con người can thiệp hay chỉnh sửa kết quả của AI để đảm bảo tính tự động hóa 100%.',
            'E': 'Mọi hệ thống AI phải được huấn luyện bí mật không công khai nguồn gốc dữ liệu.'
        },
        'answer': ['A', 'B', 'C'],
        'explanation': 'Các trụ cột cốt lõi của Responsible AI bao gồm: Minh bạch (Transparency - A), Công bằng (Fairness - B), Trách nhiệm giải trình có con người giám sát (Accountability / Human-in-the-loop - C).'
    },
    {
        'id': 'ext_17',
        'source': 'Bộ câu hỏi mở rộng - Trọng tâm Gmetrix',
        'domain_id': 4,
        'domain_name': 'Đạo đức, Pháp luật & Tác động xã hội',
        'lesson_title': 'Bài 19: Tác động xã hội và Môi trường',
        'type': 'true_false',
        'question': 'Về tác động xã hội và môi trường của AI tạo sinh, mỗi nhận định sau đúng hay sai?',
        'items': [
            {'id': 'a', 'text': 'Quá trình huấn luyện và vận hành các trung tâm dữ liệu AI tiêu thụ lượng điện năng lớn và cần hàng triệu lít nước để làm mát máy chủ.'},
            {'id': 'b', 'text': 'AI tạo sinh chỉ đe dọa các công việc lao động chân tay, hoàn toàn không ảnh hưởng đến các ngành nghề sáng tạo hay trí tuệ.'},
            {'id': 'c', 'text': 'AI tạo sinh giúp cá nhân hóa lộ trình học tập và hỗ trợ người khuyết tật tiếp cận thông tin dễ dàng hơn.'},
            {'id': 'd', 'text': 'Hiện tượng "bong bóng lọc" (filter bubble) có thể trầm trọng hơn do các thuật toán AI gợi ý nội dung phân hóa theo sở thích người dùng.'}
        ],
        'answer': {'a': True, 'b': False, 'c': True, 'd': True},
        'explanation': 'a: Đúng (vấn đề môi trường năng lượng và nước làm mát data center). b: Sai (Gen AI tác động mạnh nhất lên các công việc sáng tạo, viết lách, dịch thuật, lập trình). c: Đúng (giáo dục cá nhân hóa và công nghệ hỗ trợ trợ năng). d: Đúng (nguy cơ phân cực quan điểm xã hội).'
    },
    {
        'id': 'ext_18',
        'source': 'Bộ câu hỏi mở rộng - Trọng tâm Gmetrix',
        'domain_id': 2,
        'domain_name': 'Kỹ thuật xây dựng Prompt cơ bản',
        'lesson_title': 'Bài 8: Kỹ thuật trích xuất thông tin (Information Extraction)',
        'type': 'single_choice',
        'question': 'Bạn có một đoạn email dài từ khách hàng và muốn AI lấy ra: Tên khách hàng, Số điện thoại, Mã đơn hàng, và Vấn đề gặp phải dưới dạng JSON. Kỹ thuật prompt này thuộc nhóm nào?',
        'options': {
            'A': 'Sinh ảnh nghệ thuật (Text-to-Image).',
            'B': 'Trích xuất thông tin có cấu trúc (Structured Information Extraction).',
            'C': 'Mạng đối nghịch tạo sinh (GAN Training).',
            'D': 'Lập trình hệ điều hành (Kernel Prompting).'
        },
        'answer': 'B',
        'explanation': 'Trích xuất thông tin có cấu trúc (Information Extraction) là quá trình chuyển đổi văn bản phi cấu trúc (như email, bài báo, phản ánh khách hàng) thành dữ liệu có định dạng rõ ràng (JSON, XML, bảng) phục vụ xử lý tự động.'
    },
    {
        'id': 'ext_19',
        'source': 'Bộ câu hỏi mở rộng - Trọng tâm Gmetrix',
        'domain_id': 3,
        'domain_name': 'Tinh chỉnh Prompt & Đánh giá mô hình',
        'lesson_title': 'Bài 13: Prompting Nâng cao',
        'type': 'matching',
        'question': '(Kéo thả / Ghép nối) Ghép mỗi phương pháp tối ưu hóa hiệu quả mô hình AI với định nghĩa phù hợp:',
        'left_items': [
            {'id': '1', 'text': '1. Prompt Engineering'},
            {'id': '2', 'text': '2. RAG (Retrieval-Augmented Generation)'},
            {'id': '3', 'text': '3. Fine-tuning (Tinh chỉnh mô hình)'},
            {'id': '4', 'text': '4. Pre-training (Tiền huấn luyện)'}
        ],
        'right_items': [
            {'id': 'a', 'text': 'a. Huấn luyện mô hình từ đầu trên hàng nghìn tỷ token văn bản để học tri thức tổng quát.'},
            {'id': 'b', 'text': 'b. Thiết kế và cải thiện câu lệnh đầu vào mà không cần thay đổi trọng số mô hình.'},
            {'id': 'c', 'text': 'c. Huấn luyện tiếp mô hình đã có trên một tập dữ liệu chuyên ngành hẹp để cập nhật trọng số cho tác vụ cụ thể.'},
            {'id': 'd', 'text': 'd. Kết hợp mô hình với hệ thống tìm kiếm truy xuất tài liệu thực tế từ cơ sở dữ liệu để đưa vào prompt làm ngữ cảnh.'}
        ],
        'answer': {'1': 'b', '2': 'd', '3': 'c', '4': 'a'},
        'explanation': '1-b: Prompt Engineering tối ưu câu lệnh; 2-d: RAG truy xuất tài liệu thực tế đưa vào ngữ cảnh; 3-c: Fine-tuning cập nhật trọng số trên dữ liệu hẹp; 4-a: Pre-training huấn luyện mô hình nền tảng từ đầu.'
    },
    {
        'id': 'ext_20',
        'source': 'Bộ câu hỏi mở rộng - Trọng tâm Gmetrix',
        'domain_id': 1,
        'domain_name': 'Phương pháp và mô hình Generative AI',
        'lesson_title': 'Bài 1: Phân biệt các loại AI',
        'type': 'matching',
        'question': '(Kéo thả / Ghép nối) Ghép mỗi ví dụ ứng dụng với loại AI phù hợp nhất:',
        'left_items': [
            {'id': '1', 'text': '1. Dự báo doanh số bán máy điều nhiệt thông minh quý tới dựa trên chuỗi thời gian.'},
            {'id': '2', 'text': '2. Phát hiện và lọc email spam / không spam.'},
            {'id': '3', 'text': '3. Viết một kịch bản video quảng cáo 30 giây cho sản phẩm mới.'},
            {'id': '4', 'text': '4. Tính toán độ lệch chuẩn và trung bình thời gian phản hồi của tổng đài.'}
        ],
        'right_items': [
            {'id': 'a', 'text': 'a. Discriminative / Classification AI (AI phân loại)'},
            {'id': 'b', 'text': 'b. Statistical AI (AI thống kê)'},
            {'id': 'c', 'text': 'c. Predictive AI (AI dự đoán tương lai)'},
            {'id': 'd', 'text': 'd. Generative AI (AI tạo sinh nội dung)'}
        ],
        'answer': {'1': 'c', '2': 'a', '3': 'd', '4': 'b'},
        'explanation': '1-c: Dự báo doanh số là Predictive AI; 2-a: Lọc spam là Discriminative/Classification AI; 3-d: Viết kịch bản mới là Generative AI; 4-b: Tính độ lệch chuẩn là Statistical AI.'
    }
]

total_bank = questions + more_questions
print(f"Grand Total Questions in Bank: {len(total_bank)}")
with open('questions_db.json', 'w', encoding='utf-8') as f:
    json.dump(total_bank, f, ensure_ascii=False, indent=2)
print("Updated questions_db.json successfully!")
