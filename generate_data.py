import json
import re

# Load the 95 ebook questions
with open('ebook_valid_95.json', 'r', encoding='utf-8') as f:
    ebook_questions = json.load(f)

# Standardize ebook questions
standardized_ebook = []
for q in ebook_questions:
    standardized_ebook.append({
        'id': q['id'],
        'source': q['source'],
        'domain_id': q['domain_id'],
        'domain_name': q['domain_name'],
        'lesson_title': f"Bài {q['lesson_id']}: {q['lesson_title']}",
        'type': 'single_choice',
        'question': q['question'],
        'options': q['options'],
        'answer': q['answer'],
        'explanation': q['explanation']
    })

# 22 official Mock Exam questions
mock_questions = [
    {
        'id': 'mock_1',
        'source': 'Đề thi thử AI or Behind 2026-2027',
        'domain_id': 1,
        'domain_name': 'Phương pháp và mô hình Generative AI',
        'lesson_title': 'Bài 1: Định nghĩa AI tạo sinh',
        'type': 'single_choice',
        'question': 'Điểm khác biệt cốt lõi giữa AI tạo sinh (Generative AI) và AI dự đoán, phân loại (Predictive/Discriminative AI) là gì?',
        'options': {
            'A': 'AI tạo sinh chỉ xử lý được văn bản, còn AI dự đoán xử lý được cả hình ảnh.',
            'B': 'AI tạo sinh không cần dữ liệu để huấn luyện.',
            'C': 'AI tạo sinh tạo ra nội dung mới từ các mẫu học được trong dữ liệu; AI dự đoán, phân loại gán nhãn hoặc dự báo một giá trị từ dữ liệu đầu vào.',
            'D': 'AI dự đoán luôn cho kết quả chính xác hơn AI tạo sinh.'
        },
        'answer': 'C',
        'explanation': 'AI tạo sinh (Generative AI) học các phân phối xác suất và quy luật trong dữ liệu để sinh ra nội dung mới (văn bản, ảnh, âm thanh...). Ngược lại, AI dự đoán/phân loại (Predictive/Discriminative AI) tập trung vào việc gán nhãn, phân loại hoặc ước lượng một giá trị/kết quả từ dữ liệu đầu vào.'
    },
    {
        'id': 'mock_2',
        'source': 'Đề thi thử AI or Behind 2026-2027',
        'domain_id': 1,
        'domain_name': 'Phương pháp và mô hình Generative AI',
        'lesson_title': 'Bài 1: AI tạo sinh so với công cụ tìm kiếm',
        'type': 'single_choice',
        'question': 'So với công cụ tìm kiếm (search engine), chatbot AI tạo sinh khác ở điểm nào?',
        'options': {
            'A': 'Chatbot tổng hợp và sinh ra câu trả lời mới bằng ngôn ngữ tự nhiên, có thể sai và không phải lúc nào cũng kèm nguồn.',
            'B': 'Chatbot chỉ trả về danh sách đường liên kết tới các trang web có sẵn.',
            'C': 'Chatbot luôn cập nhật dữ liệu theo thời gian thực.',
            'D': 'Chatbot chỉ trả lời được các câu hỏi có sẵn trong cơ sở dữ liệu.'
        },
        'answer': 'A',
        'explanation': 'Công cụ tìm kiếm trả về danh sách liên kết tới trang web chứa thông tin đã có. Chatbot AI tạo sinh tổng hợp tri thức và tự viết ra câu trả lời bằng ngôn ngữ tự nhiên, có khả năng bị ảo giác (hallucination) và không mặc định trích dẫn nguồn chuẩn xác.'
    },
    {
        'id': 'mock_3',
        'source': 'Đề thi thử AI or Behind 2026-2027',
        'domain_id': 1,
        'domain_name': 'Phương pháp và mô hình Generative AI',
        'lesson_title': 'Bài 3: Các loại mô hình và thuật ngữ',
        'type': 'single_choice',
        'question': 'Kiến trúc nào là nền tảng của hầu hết các mô hình ngôn ngữ lớn (LLM) hiện nay như GPT, Gemini, Claude?',
        'options': {
            'A': 'GAN (mạng đối nghịch tạo sinh)',
            'B': 'VAE (bộ tự mã hóa biến phân)',
            'C': 'Cây quyết định (decision tree)',
            'D': 'Transformer'
        },
        'answer': 'D',
        'explanation': 'Kiến trúc Transformer (được Google giới thiệu năm 2017 với cơ chế Attention) là nền tảng cốt lõi của hầu hết các LLM tiên tiến hiện đại như GPT-4, Google Gemini, Anthropic Claude.'
    },
    {
        'id': 'mock_4',
        'source': 'Đề thi thử AI or Behind 2026-2027',
        'domain_id': 1,
        'domain_name': 'Phương pháp và mô hình Generative AI',
        'lesson_title': 'Bài 3: Siêu tham số của AI',
        'type': 'single_choice',
        'question': 'Trong nhiều công cụ AI, khi tăng tham số "nhiệt độ" (temperature) thì câu trả lời thường:',
        'options': {
            'A': 'ngắn hơn và luôn chính xác hơn.',
            'B': 'đa dạng, sáng tạo hơn nhưng kém ổn định hơn giữa các lần hỏi.',
            'C': 'được tạo nhanh hơn vì máy tính chạy ở nhiệt độ cao.',
            'D': 'luôn giống hệt nhau ở mọi lần hỏi.'
        },
        'answer': 'B',
        'explanation': 'Temperature kiểm soát tính ngẫu nhiên của mô hình: temperature thấp (gần 0) làm câu trả lời mang tính tất định, tập trung, chuẩn mực; temperature cao làm tăng tính đa dạng, bất ngờ, sáng tạo nhưng có thể kém nhất quán hoặc dễ ảo giác.'
    },
    {
        'id': 'mock_5',
        'source': 'Đề thi thử AI or Behind 2026-2027',
        'domain_id': 1,
        'domain_name': 'Phương pháp và mô hình Generative AI',
        'lesson_title': 'Bài 6: Những hạn chế của AI tạo sinh',
        'type': 'single_choice',
        'question': '“Ảo giác” (hallucination) của AI tạo sinh là hiện tượng:',
        'options': {
            'A': 'AI từ chối trả lời câu hỏi của người dùng.',
            'B': 'AI trả lời chậm do kết nối mạng yếu.',
            'C': 'AI tạo ra thông tin nghe hợp lý, trôi chảy nhưng sai hoặc không có thật, ví dụ trích dẫn một bài báo không tồn tại.',
            'D': 'AI tạo ra hình ảnh có màu sắc quá rực rỡ.'
        },
        'answer': 'C',
        'explanation': 'Ảo giác (Hallucination) là hiện tượng mô hình AI tạo ra thông tin tự tin, trôi chảy và nghe rất thuyết phục nhưng thực tế lại hoàn toàn sai sự thật hoặc không hề tồn tại.'
    },
    {
        'id': 'mock_6',
        'source': 'Đề thi thử AI or Behind 2026-2027',
        'domain_id': 1,
        'domain_name': 'Phương pháp và mô hình Generative AI',
        'lesson_title': 'Bài 2: Quy trình huấn luyện AI',
        'type': 'multi_choice',
        'question': 'Những phát biểu nào đúng về quá trình huấn luyện mô hình AI tạo sinh? (Chọn 3)',
        'required_count': 3,
        'options': {
            'A': 'Mô hình ngôn ngữ lớn cần lượng dữ liệu huấn luyện rất lớn.',
            'B': 'Sau khi huấn luyện xong, mô hình tự động cập nhật mọi sự kiện mới hằng ngày.',
            'C': 'Huấn luyện mô hình tiêu tốn nhiều năng lượng và cần các GPU mạnh.',
            'D': 'Dữ liệu huấn luyện có thể mang theo quan điểm, định kiến của người tạo ra nó.',
            'E': 'Mọi loại mô hình (tạo văn bản, tạo ảnh) đều được huấn luyện theo cùng một cách.'
        },
        'answer': ['A', 'C', 'D'],
        'explanation': 'A đúng vì LLM cần hàng tỷ đến hàng nghìn tỷ token dữ liệu. C đúng vì huấn luyện đòi hỏi cụm GPU/TPU đồ sộ tiêu thụ điện năng lớn. D đúng vì dữ liệu trên Internet có sẵn thiên kiến và định kiến con người. (B sai vì mô hình có mốc kiến thức cut-off; E sai vì tạo ảnh dùng Diffusion/GAN khác với Next-token prediction của Transformer).'
    },
    {
        'id': 'mock_7',
        'source': 'Đề thi thử AI or Behind 2026-2027',
        'domain_id': 1,
        'domain_name': 'Phương pháp và mô hình Generative AI',
        'lesson_title': 'Bài 4: Các loại đầu vào và đầu ra',
        'type': 'true_false',
        'question': 'Về đầu vào và đầu ra của các công cụ AI tạo sinh, mỗi ý sau đúng hay sai?',
        'items': [
            {'id': 'a', 'text': 'Một số công cụ nhận đầu vào là hình ảnh và tạo ra văn bản mô tả hình ảnh đó.'},
            {'id': 'b', 'text': 'Mọi công cụ AI tạo sinh đều chấp nhận cùng các loại đầu vào: văn bản, âm thanh, hình ảnh, video.'},
            {'id': 'c', 'text': 'Có công cụ chuyển một đoạn văn bản thành giọng đọc.'},
            {'id': 'd', 'text': 'AI tạo sinh chỉ tạo được văn bản, không tạo được video.'}
        ],
        'answer': {'a': True, 'b': False, 'c': True, 'd': False},
        'explanation': 'a: Đúng (Image-to-text / Image captioning). b: Sai (Nhiều công cụ chỉ nhận chuyên biệt văn bản hoặc chỉ nhận ảnh). c: Đúng (Text-to-speech). d: Sai (AI tạo sinh hiện nay tạo được video rất mạnh mẽ như Sora, Runway, InVideo).'
    },
    {
        'id': 'mock_8',
        'source': 'Đề thi thử AI or Behind 2026-2027',
        'domain_id': 1,
        'domain_name': 'Phương pháp và mô hình Generative AI',
        'lesson_title': 'Bài 6: Những hạn chế của AI tạo sinh',
        'type': 'true_false',
        'question': 'Về giới hạn của AI tạo sinh, mỗi ý sau đúng hay sai?',
        'items': [
            {'id': 'a', 'text': 'Cùng một prompt, hỏi hai lần có thể nhận được hai câu trả lời khác nhau.'},
            {'id': 'b', 'text': 'Nội dung AI tạo ra luôn đáng tin cậy nếu được viết trôi chảy, rõ ràng.'},
            {'id': 'c', 'text': 'Nếu không điều chỉnh cài đặt quyền riêng tư, cuộc trò chuyện có thể được dùng để huấn luyện mô hình.'},
            {'id': 'd', 'text': 'Hiện đã có một bộ tiêu chuẩn chung, bắt buộc trên toàn thế giới cho mọi cách sử dụng AI tạo sinh.'}
        ],
        'answer': {'a': True, 'b': False, 'c': True, 'd': False},
        'explanation': 'a: Đúng (do tính ngẫu nhiên của mô hình xác suất khi temperature > 0). b: Sai (văn phong trôi chảy vẫn có thể là ảo giác hoặc thông tin sai). c: Đúng (nhiều nền tảng mặc định thu thập dữ liệu hội thoại trừ khi tắt trong cài đặt riêng tư). d: Sai (các quốc gia và khu vực có khung pháp lý riêng như EU AI Act, chưa có luật toàn cầu bắt buộc chung duy nhất).'
    },
    {
        'id': 'mock_9',
        'source': 'Đề thi thử AI or Behind 2026-2027',
        'domain_id': 1,
        'domain_name': 'Phương pháp và mô hình Generative AI',
        'lesson_title': 'Bài 3: Các thuật ngữ chính',
        'type': 'matching',
        'question': '(Kéo thả / Ghép nối) Ghép mỗi thuật ngữ ở cột trái với định nghĩa phù hợp ở cột phải (có 1 định nghĩa thừa không dùng đến):',
        'left_items': [
            {'id': '1', 'text': '1. Token'},
            {'id': '2', 'text': '2. Tập dữ liệu (dataset)'},
            {'id': '3', 'text': '3. Mạng nơ-ron (neural network)'},
            {'id': '4', 'text': '4. Mạng nơ-ron tích chập (CNN)'}
        ],
        'right_items': [
            {'id': 'a', 'text': 'a. Mô hình gồm nhiều lớp "nơ-ron" nhân tạo liên kết với nhau, học từ dữ liệu bằng cách điều chỉnh trọng số.'},
            {'id': 'b', 'text': 'b. Đơn vị văn bản nhỏ (một từ, một phần của từ hoặc dấu câu) mà mô hình ngôn ngữ xử lý.'},
            {'id': 'c', 'text': 'c. Loại mạng nơ-ron xử lý hình ảnh hiệu quả nhờ các bộ lọc quét qua từng vùng ảnh.'},
            {'id': 'd', 'text': 'd. Tập hợp văn bản, hình ảnh… được dùng để huấn luyện mô hình.'},
            {'id': 'e', 'text': 'e. Câu lệnh người dùng nhập để yêu cầu AI thực hiện một nhiệm vụ (thừa - định nghĩa của Prompt).'}
        ],
        'answer': {'1': 'b', '2': 'd', '3': 'a', '4': 'c'},
        'explanation': '1-b (Token là đơn vị văn bản nhỏ); 2-d (Dataset là tập hợp dữ liệu huấn luyện); 3-a (Neural network gồm các lớp nơ-ron liên kết điều chỉnh trọng số); 4-c (CNN dùng bộ lọc tích chập để xử lý ảnh); e là định nghĩa của Prompt (thừa).'
    },
    {
        'id': 'mock_10',
        'source': 'Đề thi thử AI or Behind 2026-2027',
        'domain_id': 1,
        'domain_name': 'Phương pháp và mô hình Generative AI',
        'lesson_title': 'Bài 3: Mô hình Diffusion',
        'type': 'visual',
        'image_url': 'app_assets/page_5_Image29.png',
        'question': '(Lựa chọn hình ảnh) Quan sát hình ảnh bên dưới. Hình nào mô tả đúng cách mô hình khuếch tán (diffusion) tạo ra một ảnh mới theo prompt?',
        'options': {
            'A': 'Hình A: Bắt đầu từ văn bản và ghép các mảnh ảnh có sẵn lại với nhau.',
            'B': 'Hình B: Bắt đầu từ nhiễu ngẫu nhiên (noise) và dần dần loại bỏ nhiễu qua các bước (denoising) để hình thành bức ảnh rõ nét.',
            'C': 'Hình C: Cắt lớp ảnh từ trên xuống dưới theo từng đường quét ngang.',
            'D': 'Hình D: Phóng to các điểm ảnh nhỏ cho đến khi đạt độ phân giải cao.'
        },
        'answer': 'B',
        'explanation': 'Mô hình Diffusion hoạt động theo cơ chế khử nhiễu (Denoising Process): bắt đầu từ một ma trận nhiễu Gauss ngẫu nhiên (pure random noise) và qua từng bước lặp lại sẽ tinh chỉnh loại bỏ nhiễu có định hướng theo văn bản gợi ý để sinh ra bức ảnh hoàn chỉnh.'
    },
    {
        'id': 'mock_11',
        'source': 'Đề thi thử AI or Behind 2026-2027',
        'domain_id': 2,
        'domain_name': 'Kỹ thuật xây dựng Prompt cơ bản',
        'lesson_title': 'Bài 7: Xác định câu lệnh',
        'type': 'single_choice',
        'question': 'Prompt nào hiệu quả nhất để nhờ AI tóm tắt một bài báo khoa học dài cho học sinh lớp 10?',
        'options': {
            'A': '“Tóm tắt.”',
            'B': '“Tóm tắt bài này cho dễ hiểu.”',
            'C': '“Bạn là giáo viên Sinh học. Hãy tóm tắt bài báo dưới đây thành 5 ý chính, mỗi ý không quá 2 câu, dùng ngôn ngữ phù hợp với học sinh lớp 10 và giải thích các thuật ngữ khó. [nội dung bài báo]”',
            'D': '“Viết lại toàn bộ bài báo dưới đây cho hay hơn.”'
        },
        'answer': 'C',
        'explanation': 'Prompt C có đầy đủ 4 yếu tố then chốt của một prompt chuẩn: Gán vai trò (Persona - Giáo viên Sinh học), Nhiệm vụ cụ thể (5 ý chính, <= 2 câu), Đối tượng người đọc (Học sinh lớp 10, giải thích từ khó), và Đính kèm dữ liệu nguồn rõ ràng.'
    },
    {
        'id': 'mock_12',
        'source': 'Đề thi thử AI or Behind 2026-2027',
        'domain_id': 3,
        'domain_name': 'Tinh chỉnh Prompt & Đánh giá mô hình',
        'lesson_title': 'Bài 13: Các kỹ thuật câu lệnh nâng cao',
        'type': 'single_choice',
        'question': 'Trước khi nhờ AI viết bài nghị luận về tác hại của vi nhựa, bạn yêu cầu AI “liệt kê 5 sự thật khoa học quan trọng về vi nhựa”, rồi dùng chính danh sách đó làm cơ sở để viết bài. Đây là kỹ thuật:',
        'options': {
            'A': 'Zero-shot prompting',
            'B': 'Tạo tri thức trước (Generated knowledge prompting)',
            'C': 'Prompt ngược (Reverse prompting)',
            'D': 'Gán vai trò (Persona)'
        },
        'answer': 'B',
        'explanation': 'Generated Knowledge Prompting (Tạo tri thức trước) là kỹ thuật yêu cầu mô hình tự tạo ra các sự thật/thông tin liên quan trước, sau đó dùng chính các thông tin đó làm ngữ cảnh để hoàn thành nhiệm vụ phức tạp tiếp theo.'
    },
    {
        'id': 'mock_13',
        'source': 'Đề thi thử AI or Behind 2026-2027',
        'domain_id': 3,
        'domain_name': 'Tinh chỉnh Prompt & Đánh giá mô hình',
        'lesson_title': 'Bài 13: Chain-of-thought',
        'type': 'single_choice',
        'question': 'Yêu cầu AI “hãy suy luận từng bước trước khi đưa ra đáp án” khi giải một bài toán là kỹ thuật:',
        'options': {
            'A': 'Chuỗi suy luận (Chain-of-thought)',
            'B': 'Few-shot prompting',
            'C': 'Tự nhất quán (Self-consistency)',
            'D': 'Prompt ngược (Reverse prompting)'
        },
        'answer': 'A',
        'explanation': 'Chain-of-Thought (CoT - Chuỗi suy luận) hướng dẫn mô hình phân tích bài toán thành các bước lý giải trung gian trước khi kết luận, giúp tăng độ chính xác đáng kể trong các bài toán logic, số học và lập luận.'
    },
    {
        'id': 'mock_14',
        'source': 'Đề thi thử AI or Behind 2026-2027',
        'domain_id': 3,
        'domain_name': 'Tinh chỉnh Prompt & Đánh giá mô hình',
        'lesson_title': 'Bài 12: Thêm đầu vào vào câu lệnh',
        'type': 'single_choice',
        'question': 'Khi dịch tài liệu chuyên ngành bằng AI, đầu vào bổ sung nào giúp thuật ngữ được dịch nhất quán nhất?',
        'options': {
            'A': 'Yêu cầu AI dịch nhanh hơn.',
            'B': 'Chụp tài liệu thành nhiều file ảnh rồi gửi lần lượt.',
            'C': 'Xóa hết các thuật ngữ khó trước khi dịch.',
            'D': 'Cung cấp bảng thuật ngữ (glossary) kèm cách dịch mong muốn.'
        },
        'answer': 'D',
        'explanation': 'Cung cấp bảng thuật ngữ (Glossary / Terminology list) trong prompt giúp neo chặt cách dịch các từ khóa chuyên ngành, tránh việc AI dịch mỗi đoạn một kiểu không đồng nhất.'
    },
    {
        'id': 'mock_15',
        'source': 'Đề thi thử AI or Behind 2026-2027',
        'domain_id': 3,
        'domain_name': 'Tinh chỉnh Prompt & Đánh giá mô hình',
        'lesson_title': 'Bài 13: Reverse Prompting',
        'type': 'single_choice',
        'question': '“Prompt ngược” (reverse prompting) là cách:',
        'options': {
            'A': 'viết prompt theo thứ tự ngược từ cuối lên đầu.',
            'B': 'đưa cho AI một sản phẩm mẫu (bài viết, bức ảnh…) và yêu cầu AI viết ra prompt có thể tạo ra sản phẩm tương tự.',
            'C': 'yêu cầu AI trả lời bằng một ngôn ngữ khác.',
            'D': 'xóa lịch sử trò chuyện rồi hỏi lại từ đầu.'
        },
        'answer': 'B',
        'explanation': 'Reverse Prompting (Prompt ngược) là kỹ thuật cung cấp đầu ra mong muốn (văn bản mẫu, hình ảnh mẫu) và nhờ AI giải mã, suy luận ngược lại câu prompt tối ưu có thể tạo ra sản phẩm tương tự.'
    },
    {
        'id': 'mock_16',
        'source': 'Đề thi thử AI or Behind 2026-2027',
        'domain_id': 2,
        'domain_name': 'Kỹ thuật xây dựng Prompt cơ bản',
        'lesson_title': 'Bài 11: Cải thiện câu lệnh',
        'type': 'multi_choice',
        'question': 'Một bạn gõ prompt “Viết bài về CLB” và nhận được kết quả chung chung. Hai cách cải thiện hiệu quả nhất là gì? (Chọn 2)',
        'required_count': 2,
        'options': {
            'A': 'Viết tắt nhiều hơn để prompt ngắn gọn.',
            'B': 'Nêu rõ ngữ cảnh: CLB gì, của trường nào, bài đăng ở đâu, ai sẽ đọc.',
            'C': 'Gõ lại đúng prompt cũ nhiều lần đến khi kết quả tốt hơn.',
            'D': 'Nêu yêu cầu về giọng văn, độ dài và định dạng, ví dụ “150 chữ, giọng vui tươi, kèm 3 hashtag”.',
            'E': 'Giả định AI đã biết rõ CLB của mình.'
        },
        'answer': ['B', 'D'],
        'explanation': 'Để cải thiện một prompt chung chung, hai biện pháp hàng đầu là: cung cấp ngữ cảnh cụ thể (CLB nào, đối tượng người đọc là ai) và quy định rõ ràng định dạng/giọng điệu/độ dài của bài viết.'
    },
    {
        'id': 'mock_17',
        'source': 'Đề thi thử AI or Behind 2026-2027',
        'domain_id': 2,
        'domain_name': 'Kỹ thuật xây dựng Prompt cơ bản',
        'lesson_title': 'Bài 8: Câu lệnh chuyển đổi nội dung',
        'type': 'multi_choice',
        'question': 'Những prompt nào thuộc nhóm “chuyển đổi nội dung” (transform content)? (Chọn 2)',
        'required_count': 2,
        'options': {
            'A': '“Chuyển đoạn văn sau thành bảng so sánh 3 cột.”',
            'B': '“Liệt kê 10 ý tưởng đặt tên cho đội thi.”',
            'C': '“Dịch email sau sang tiếng Anh, giữ giọng trang trọng.”',
            'D': '“Thủ đô của Australia là thành phố nào?”'
        },
        'answer': ['A', 'C'],
        'explanation': 'Chuyển đổi nội dung (Transform Content) nhận đầu vào có sẵn và biến đổi hình thức/ngôn ngữ (như định dạng lại bảng, dịch thuật, tóm tắt). B là tạo ý tưởng mới (Ideation), D là truy vấn thông tin (Information retrieval).'
    },
    {
        'id': 'mock_18',
        'source': 'Đề thi thử AI or Behind 2026-2027',
        'domain_id': 3,
        'domain_name': 'Tinh chỉnh Prompt & Đánh giá mô hình',
        'lesson_title': 'Bài 11: Cải thiện câu lệnh',
        'type': 'true_false',
        'question': 'Về việc tinh chỉnh prompt, mỗi ý sau đúng hay sai?',
        'items': [
            {'id': 'a', 'text': 'Gán vai trò cho AI, ví dụ “Bạn là hướng dẫn viên du lịch”, giúp câu trả lời phù hợp hơn với mục đích.'},
            {'id': 'b', 'text': 'Nên dùng nhiều từ viết tắt để AI hiểu nhanh hơn.'},
            {'id': 'c', 'text': 'Trong cùng một cuộc trò chuyện, AI có thể dựa vào các trao đổi trước đó để trả lời.'},
            {'id': 'd', 'text': 'Prompt càng dài thì kết quả chắc chắn càng tốt.'}
        ],
        'answer': {'a': True, 'b': False, 'c': True, 'd': False},
        'explanation': 'a: Đúng (Persona định hình phong cách và góc nhìn). b: Sai (Viết tắt gây mập mờ, dễ làm AI hiểu sai). c: Đúng (AI duy trì bộ nhớ ngữ cảnh trong cùng phiên). d: Sai (Prompt dài dòng, chứa thông tin mâu thuẫn sẽ làm giảm chất lượng đầu ra).'
    },
    {
        'id': 'mock_19',
        'source': 'Đề thi thử AI or Behind 2026-2027',
        'domain_id': 2,
        'domain_name': 'Kỹ thuật xây dựng Prompt cơ bản',
        'lesson_title': 'Quy trình làm việc với AI',
        'type': 'ordering',
        'question': '(Sắp xếp) Sắp xếp các bước làm việc với AI tạo sinh theo trình tự hợp lý từ đầu đến cuối:',
        'items': [
            {'id': 'A', 'text': 'Đọc và đánh giá kết quả đầu tiên.'},
            {'id': 'B', 'text': 'Xác định rõ mục tiêu và sản phẩm cần có.'},
            {'id': 'C', 'text': 'Tinh chỉnh prompt, rồi kiểm chứng kết quả cuối cùng.'},
            {'id': 'D', 'text': 'Viết prompt đầu tiên có đủ ngữ cảnh, nhiệm vụ và định dạng mong muốn.'},
            {'id': 'E', 'text': 'Sử dụng sản phẩm và ghi chú rõ việc có dùng AI.'}
        ],
        'answer': ['B', 'D', 'A', 'C', 'E'],
        'explanation': 'Quy trình chuẩn: (B) Xác định mục tiêu -> (D) Soạn prompt ban đầu -> (A) Đánh giá kết quả -> (C) Tinh chỉnh và kiểm chứng độ chính xác -> (E) Ứng dụng sản phẩm kèm ghi nhận minh bạch (Responsible AI).'
    },
    {
        'id': 'mock_20',
        'source': 'Đề thi thử AI or Behind 2026-2027',
        'domain_id': 3,
        'domain_name': 'Tinh chỉnh Prompt & Đánh giá mô hình',
        'lesson_title': 'Bài 13: Các kỹ thuật prompt',
        'type': 'matching',
        'question': '(Kéo thả / Ghép nối) Ghép mỗi kỹ thuật prompt ở cột trái với ví dụ cụ thể phù hợp ở cột phải:',
        'left_items': [
            {'id': '1', 'text': '1. Zero-shot'},
            {'id': '2', 'text': '2. Few-shot'},
            {'id': '3', 'text': '3. Dùng mẫu (template)'},
            {'id': '4', 'text': '4. Gán vai trò (persona)'}
        ],
        'right_items': [
            {'id': 'a', 'text': 'a. “Trình bày kết quả theo mẫu: Tên loài – Đặc điểm nhận dạng – Môi trường sống.”'},
            {'id': 'b', 'text': 'b. “\'Món này ngon tuyệt\' → Tích cực; \'Phục vụ quá chậm\' → Tiêu cực. Vậy \'Giá hơi cao nhưng đáng tiền\' → ?”'},
            {'id': 'c', 'text': 'c. “Bạn là nhà tuyển dụng. Hãy nhận xét CV sau và chỉ ra 3 điểm cần sửa.”'},
            {'id': 'd', 'text': 'd. “Phân loại cảm xúc của câu sau: \'Hôm nay trời đẹp quá!\'”'}
        ],
        'answer': {'1': 'd', '2': 'b', '3': 'a', '4': 'c'},
        'explanation': '1-d (Zero-shot không kèm ví dụ mẫu); 2-b (Few-shot cung cấp các cặp ví dụ mẫu có nhãn trước); 3-a (Template quy định sẵn mẫu định dạng đầu ra); 4-c (Persona gán vai trò nhà tuyển dụng).'
    },
    {
        'id': 'mock_21',
        'source': 'Đề thi thử AI or Behind 2026-2027',
        'domain_id': 2,
        'domain_name': 'Kỹ thuật xây dựng Prompt cơ bản',
        'lesson_title': 'Bài 9: Câu lệnh hình ảnh',
        'type': 'matching',
        'question': '(Kéo thả / Ghép nối) Cho prompt tạo ảnh: “Một học sinh đang đọc sách dưới gốc cây phượng, phong cách tranh màu nước, ánh nắng chiều, tỷ lệ khung hình 16:9.” Ghép mỗi cụm từ ở cột trái với vai trò trong prompt ở cột phải (có 1 vai trò thừa):',
        'left_items': [
            {'id': '1', 'text': '1. “Một học sinh đang đọc sách”'},
            {'id': '2', 'text': '2. “dưới gốc cây phượng”'},
            {'id': '3', 'text': '3. “phong cách tranh màu nước”'},
            {'id': '4', 'text': '4. “tỷ lệ khung hình 16:9”'}
        ],
        'right_items': [
            {'id': 'a', 'text': 'a. Phong cách nghệ thuật (Art style)'},
            {'id': 'b', 'text': 'b. Thông số định dạng đầu ra (Output format / Aspect ratio)'},
            {'id': 'c', 'text': 'c. Chủ thể và hành động (Subject & Action)'},
            {'id': 'd', 'text': 'd. Bối cảnh, địa điểm (Setting / Location)'},
            {'id': 'e', 'text': 'e. Ánh sáng (Lighting) — vai trò thừa'}
        ],
        'answer': {'1': 'c', '2': 'd', '3': 'a', '4': 'b'},
        'explanation': '1-c (Chủ thể: học sinh đang đọc sách); 2-d (Bối cảnh: dưới gốc cây phượng); 3-a (Phong cách: màu nước); 4-b (Định dạng: tỷ lệ 16:9); e (Ánh sáng) là mục thừa.'
    },
    {
        'id': 'mock_22',
        'source': 'Đề thi thử AI or Behind 2026-2027',
        'domain_id': 3,
        'domain_name': 'Tinh chỉnh Prompt & Đánh giá mô hình',
        'lesson_title': 'Bài 16: Chuỗi câu lệnh (Prompt Chaining)',
        'type': 'visual',
        'image_url': 'app_assets/page_9_Image38.png',
        'question': '(Lựa chọn sơ đồ) Quan sát sơ đồ bên dưới. Sơ đồ nào mô tả đúng kỹ thuật chuỗi prompt (prompt chaining)?',
        'options': {
            'A': 'Sơ đồ A: Nhập nhiều câu hỏi hoàn toàn độc lập vào các cửa sổ chat khác nhau.',
            'B': 'Sơ đồ B: Lặp đi lặp lại một câu prompt duy nhất cho đến khi AI trả lời đúng.',
            'C': 'Sơ đồ C: Chia bài toán phức tạp thành chuỗi các bước tuần tự, trong đó kết quả đầu ra của bước trước làm đầu vào cho bước tiếp theo.',
            'D': 'Sơ đồ D: Ghép tất cả các câu lệnh vào một đoạn văn bản dài duy nhất không phân cách.'
        },
        'answer': 'C',
        'explanation': 'Prompt Chaining (Chuỗi câu lệnh) là kỹ thuật chia tách quy trình phức tạp thành một chuỗi các prompt nhỏ tuần tự: Output của Prompt 1 được xử lý hoặc làm Context/Input cho Prompt 2, giúp kiểm soát chất lượng từng bước và hạn chế sai số tích lũy.'
    }
]

# Additional High-Yield Questions synthesized from Teacher Guide & Practice Exercises
# Covering diverse types (multi-choice, true/false, matching, ordering)
extra_questions = [
    {
        'id': 'ext_1',
        'source': 'Gen AI Teacher Guide & Certiport Objectives',
        'domain_id': 4,
        'domain_name': 'Đạo đức, Pháp luật & Tác động xã hội',
        'lesson_title': 'Bài 17: Bản quyền và Quyền sở hữu trí tuệ',
        'type': 'single_choice',
        'question': 'Theo đa số các cơ quan bản quyền hiện nay (như Cục Bản quyền Hoa Kỳ - USCO), tác phẩm hoàn toàn do AI tạo sinh sinh ra mà không có sự can thiệp sáng tạo đáng kể của con người thì:',
        'options': {
            'A': 'Tự động thuộc bản quyền của công ty phát triển mô hình AI.',
            'B': 'Không được bảo hộ bản quyền tác giả vì bản quyền chỉ cấp cho sáng tạo của con người.',
            'C': 'Thuộc bản quyền chung của toàn nhân loại và cấm sử dụng cho mục đích thương mại.',
            'D': 'Tự động cấp bản quyền cho người nhập câu lệnh prompt đầu tiên.'
        },
        'answer': 'B',
        'explanation': 'Theo quy định hiện hành của hầu hết các cơ quan bản quyền quốc tế, bản quyền chỉ bảo hộ sản phẩm do trí tuệ con người sáng tạo (Human authorship). Một tác phẩm thuần túy do máy móc/AI sinh ra không đáp ứng tiêu chuẩn tác giả con người nên không được cấp bản quyền.'
    },
    {
        'id': 'ext_2',
        'source': 'Gen AI Teacher Guide & Certiport Objectives',
        'domain_id': 4,
        'domain_name': 'Đạo đức, Pháp luật & Tác động xã hội',
        'lesson_title': 'Bài 17: Quyền riêng tư và Thông tin cá nhân (PII)',
        'type': 'multi_choice',
        'question': 'Những thông tin nào dưới đây thuộc nhóm Thông tin định danh cá nhân (PII - Personally Identifiable Information) TUYỆT ĐỐI KHÔNG NÊN nhập vào các công cụ AI công cộng? (Chọn 3)',
        'required_count': 3,
        'options': {
            'A': 'Số Căn cước công dân / Số An sinh xã hội (SSN).',
            'B': 'Thông tin thẻ tín dụng, tài khoản ngân hàng và mật khẩu.',
            'C': 'Lịch sử bệnh án và hồ sơ sức khỏe cá nhân chi tiết.',
            'D': 'Tên một danh lam thắng cảnh bạn dự định tham quan.',
            'E': 'Một đoạn văn trích từ tác phẩm văn học kinh điển thế giới.'
        },
        'answer': ['A', 'B', 'C'],
        'explanation': 'PII bao gồm CCCD/CMND, số tài khoản ngân hàng, thẻ tín dụng, hồ sơ bệnh án cá nhân... Khi nhập vào chatbot AI công cộng, các dữ liệu này có thể bị lưu vào máy chủ của bên thứ ba hoặc vô tình rò rỉ trong quá trình huấn luyện mô hình.'
    },
    {
        'id': 'ext_3',
        'source': 'Gen AI Teacher Guide & Certiport Objectives',
        'domain_id': 4,
        'domain_name': 'Đạo đức, Pháp luật & Tác động xã hội',
        'lesson_title': 'Bài 18: Rủi ro của AI tạo sinh',
        'type': 'true_false',
        'question': 'Về các rủi ro an ninh và xã hội của AI tạo sinh, mỗi nhận định sau đúng hay sai?',
        'items': [
            {'id': 'a', 'text': 'Deepfake có thể được kẻ xấu lợi dụng để tạo video, âm thanh giả mạo lãnh đạo công ty nhằm lừa đảo chuyển tiền.'},
            {'id': 'b', 'text': 'AI tạo sinh giúp kẻ tấn công mạng dễ dàng soạn thảo các email lừa đảo (phishing) tinh vi, chuẩn ngữ pháp và khó nhận biết hơn.'},
            {'id': 'c', 'text': 'Mọi hình ảnh do AI tạo sinh tạo ra đều có watermark chống giả mạo mà con người không thể xóa được.'},
            {'id': 'd', 'text': 'Sử dụng AI có thể gây nguy cơ vi phạm bí mật kinh doanh nếu nhân viên đưa mã nguồn nội bộ lên công cụ AI bên ngoài.'}
        ],
        'answer': {'a': True, 'b': True, 'c': False, 'd': True},
        'explanation': 'a: Đúng (Deepfake mạo danh CEO/người thân lừa đảo tài chính). b: Đúng (AI giúp tin tặc viết email lừa đảo không còn lỗi chính tả ngô nghê). c: Sai (Nhiều công cụ mã nguồn mở không gán watermark hoặc watermark dễ bị gỡ bỏ). d: Đúng (Nhiều tập đoàn như Samsung, Apple từng cấm dùng ChatGPT vì sự cố lộ mã nguồn bí mật).'
    },
    {
        'id': 'ext_4',
        'source': 'Gen AI Teacher Guide & Certiport Objectives',
        'domain_id': 4,
        'domain_name': 'Đạo đức, Pháp luật & Tác động xã hội',
        'lesson_title': 'Bài 18: Rủi ro và Đạo đức AI',
        'type': 'matching',
        'question': '(Kéo thả / Ghép nối) Ghép mỗi thuật ngữ rủi ro AI ở cột trái với ví dụ hoặc mô tả tương ứng ở cột phải:',
        'left_items': [
            {'id': '1', 'text': '1. Deepfake'},
            {'id': '2', 'text': '2. Thiên vị / Định kiến (Bias)'},
            {'id': '3', 'text': '3. Nhiễm độc dữ liệu (Data Poisoning)'},
            {'id': '4', 'text': '4. Ảo giác (Hallucination)'}
        ],
        'right_items': [
            {'id': 'a', 'text': 'a. AI tạo ra kết quả thiên lệch, ví dụ luôn miêu tả bác sĩ là nam giới và y tá là nữ giới do dữ liệu huấn luyện mất cân bằng.'},
            {'id': 'b', 'text': 'b. Công nghệ ghép khuôn mặt, giọng nói của người thật vào một video hoặc đoạn ghi âm với hành động họ chưa từng làm.'},
            {'id': 'c', 'text': 'c. Kẻ xấu cố tình chèn dữ liệu độc hại hoặc sai lệch vào tập dữ liệu huấn luyện để làm sai lệch hành vi của mô hình.'},
            {'id': 'd', 'text': 'd. Mô hình tự bịa ra một điều luật hoặc một số liệu nghiên cứu không hề tồn tại nhưng khẳng định chắc nịch.'}
        ],
        'answer': {'1': 'b', '2': 'a', '3': 'c', '4': 'd'},
        'explanation': '1-b: Deepfake là giả mạo âm thanh/hình ảnh con người; 2-a: Bias là thiên vị định kiến xã hội từ dữ liệu; 3-c: Data Poisoning là phá hoại tập huấn luyện; 4-d: Hallucination là bịa thông tin sai sự thật.'
    },
    {
        'id': 'ext_5',
        'source': 'Gen AI Teacher Guide & Certiport Objectives',
        'domain_id': 3,
        'domain_name': 'Tinh chỉnh Prompt & Đánh giá mô hình',
        'lesson_title': 'Bài 14: Quy trình kiểm chứng thông tin (Fact-Checking)',
        'type': 'ordering',
        'question': '(Sắp xếp) Khi nhận được một báo cáo nghiên cứu thị trường do AI tạo ra, sắp xếp quy trình kiểm chứng thông tin hợp lý nhất:',
        'items': [
            {'id': 'A', 'text': 'Sử dụng máy tính hoặc công thức độc lập để tính toán lại toàn bộ các con số thống kê, tỷ lệ %.'},
            {'id': 'B', 'text': 'Đọc lướt để phát hiện các dấu hiệu mơ hồ, mâu thuẫn nội tại hoặc câu khẳng định thiếu căn cứ.'},
            {'id': 'C', 'text': 'Truy vấn các nguồn chính thống độc lập (báo cáo ngành, cơ quan nhà nước, trang web chính thức) để đối chiếu.'},
            {'id': 'D', 'text': 'Ghi chú nguồn gốc và chỉ số tin cậy vào bản báo cáo cuối cùng trước khi gửi cho ban lãnh đạo.'}
        ],
        'answer': ['B', 'A', 'C', 'D'],
        'explanation': 'Trình tự thẩm định chuẩn: (B) Đọc rà soát ban đầu để phát hiện điểm nghi vấn -> (A) Tự tính lại các số liệu toán học -> (C) Đối chiếu chéo (Cross-check) với các nguồn dữ liệu độc lập có thẩm quyền -> (D) Hoàn thiện tài liệu với ghi chú nguồn rõ ràng.'
    },
    {
        'id': 'ext_6',
        'source': 'Gen AI Teacher Guide & Certiport Objectives',
        'domain_id': 2,
        'domain_name': 'Kỹ thuật xây dựng Prompt cơ bản',
        'lesson_title': 'Bài 7: Các thành phần của một Prompt hiệu quả',
        'type': 'matching',
        'question': '(Kéo thả / Ghép nối) Ghép mỗi thành phần cốt lõi của Prompting Framework với vai trò tương ứng của nó:',
        'left_items': [
            {'id': '1', 'text': '1. Role / Persona (Vai trò)'},
            {'id': '2', 'text': '2. Task / Instruction (Nhiệm vụ)'},
            {'id': '3', 'text': '3. Context (Ngữ cảnh)'},
            {'id': '4', 'text': '4. Constraints / Format (Ràng buộc & Định dạng)'}
        ],
        'right_items': [
            {'id': 'a', 'text': 'a. Cung cấp bối cảnh nền tảng, tình huống thực tế hoặc tài liệu tham khảo để AI nắm bắt vấn đề.'},
            {'id': 'b', 'text': 'b. Định hình phong cách, góc nhìn chuyên môn và giọng điệu mà AI sẽ sử dụng khi giao tiếp.'},
            {'id': 'c', 'text': 'c. Quy định cụ thể độ dài (dưới 200 từ), cấu trúc trình bày (bảng Markdown, gạch đầu dòng) và những điều bị cấm.'},
            {'id': 'd', 'text': 'd. Hành động cụ thể và mục tiêu chính mà người dùng muốn AI thực hiện (tóm tắt, phân tích, viết mã...).'}
        ],
        'answer': {'1': 'b', '2': 'd', '3': 'a', '4': 'c'},
        'explanation': '1-b: Persona định hình chuyên gia/giọng điệu; 2-d: Task là yêu cầu hành động chính; 3-a: Context là bối cảnh tài liệu; 4-c: Constraints/Format là giới hạn số từ và quy chuẩn hiển thị.'
    },
    {
        'id': 'ext_7',
        'source': 'Gen AI Teacher Guide & Certiport Objectives',
        'domain_id': 1,
        'domain_name': 'Phương pháp và mô hình Generative AI',
        'lesson_title': 'Bài 5: Lựa chọn công cụ phù hợp với nhiệm vụ',
        'type': 'matching',
        'question': '(Kéo thả / Ghép nối) Ghép mỗi công cụ AI phổ biến với lĩnh vực thế mạnh vượt trội của nó:',
        'left_items': [
            {'id': '1', 'text': '1. Midjourney / Stable Diffusion'},
            {'id': '2', 'text': '2. ElevenLabs'},
            {'id': '3', 'text': '3. GitHub Copilot / Cursor'},
            {'id': '4', 'text': '4. Suno / Udio'}
        ],
        'right_items': [
            {'id': 'a', 'text': 'a. Lập trình, viết mã nguồn, gỡ lỗi và tự động hoàn thành code.'},
            {'id': 'b', 'text': 'b. Tạo ảnh nghệ thuật chất lượng cao từ mô tả văn bản (Text-to-Image).'},
            {'id': 'c', 'text': 'c. Tạo bài hát hoàn chỉnh (lời, giai điệu, hòa âm phối khí) từ gợi ý văn bản.'},
            {'id': 'd', 'text': 'd. Chuyển văn bản thành giọng đọc tự nhiên (Text-to-Speech) và nhân bản giọng nói (Voice Cloning).'}
        ],
        'answer': {'1': 'b', '2': 'd', '3': 'a', '4': 'c'},
        'explanation': '1-b: Midjourney/Stable Diffusion chuyên tạo ảnh; 2-d: ElevenLabs chuyên về giọng đọc và nhân bản âm thanh; 3-a: Copilot chuyên hỗ trợ code phần mềm; 4-c: Suno/Udio chuyên sáng tác âm nhạc.'
    },
    {
        'id': 'ext_8',
        'source': 'Gen AI Teacher Guide & Certiport Objectives',
        'domain_id': 1,
        'domain_name': 'Phương pháp và mô hình Generative AI',
        'lesson_title': 'Bài 2: Kiến trúc phần cứng trong huấn luyện AI',
        'type': 'single_choice',
        'question': 'Tại sao các đơn vị xử lý đồ họa (GPU) và bộ xử lý tensor (TPU) lại vượt trội hơn hẳn bộ vi xử lý trung tâm (CPU) trong việc huấn luyện các mô hình AI tạo sinh lớn?',
        'options': {
            'A': 'Vì GPU có dung lượng ổ cứng lưu trữ lớn hơn nhiều so với CPU.',
            'B': 'Vì GPU được tối ưu hóa cho kiến trúc song song khổng lồ với hàng nghìn lõi tính toán đồng thời các phép tính ma trận.',
            'C': 'Vì GPU không cần nguồn điện mà sử dụng năng lượng từ tính.',
            'D': 'Vì CPU không có khả năng hiểu các thuật toán học máy.'
        },
        'answer': 'B',
        'explanation': 'Huấn luyện mạng nơ-ron sâu chủ yếu bao gồm hàng tỷ phép nhân và cộng ma trận. CPU được thiết kế với ít lõi để xử lý tuần tự linh hoạt, trong khi GPU/TPU sở hữu hàng nghìn đến hàng chục nghìn lõi tính toán song song cực kỳ hiệu quả cho ma trận số thực.'
    },
    {
        'id': 'ext_9',
        'source': 'Gen AI Teacher Guide & Certiport Objectives',
        'domain_id': 3,
        'domain_name': 'Tinh chỉnh Prompt & Đánh giá mô hình',
        'lesson_title': 'Bài 12: Kỹ thuật phân cách (Delimiters)',
        'type': 'single_choice',
        'question': 'Trong kỹ thuật viết Prompt, việc sử dụng các ký tự phân cách (delimiters) như dấu ngoặc kép ba ("""), dấu ba gạch ngang (---), hoặc thẻ XML (<context>...</context>) nhằm mục đích chính nào?',
        'options': {
            'A': 'Làm cho prompt hiển thị đẹp mắt hơn trên giao diện người dùng.',
            'B': 'Giúp AI phân biệt rõ ràng giữa câu lệnh chỉ dẫn của bạn và đoạn văn bản dữ liệu đầu vào cần xử lý.',
            'C': 'Tăng tốc độ kết nối Internet của mô hình máy chủ.',
            'D': 'Kích hoạt chế độ kiểm tra chính tả tự động của AI.'
        },
        'answer': 'B',
        'explanation': 'Ký tự phân cách (Delimiters) giúp mô hình phân định ranh giới rành mạch giữa câu lệnh điều khiển (Instructions) và nội dung tài liệu/ngữ cảnh (Context/Data), ngăn ngừa hiện tượng Prompt Injection và giúp AI không nhầm dữ liệu thành câu lệnh.'
    },
    {
        'id': 'ext_10',
        'source': 'Gen AI Teacher Guide & Certiport Objectives',
        'domain_id': 2,
        'domain_name': 'Kỹ thuật xây dựng Prompt cơ bản',
        'lesson_title': 'Bài 9: Kỹ thuật Negative Prompt',
        'type': 'single_choice',
        'question': 'Trong các công cụ tạo hình ảnh như Stable Diffusion hoặc Midjourney, tham số "Negative Prompt" (câu lệnh phủ định) được dùng để:',
        'options': {
            'A': 'Tạo ra các bức ảnh mang màu sắc tối tăm hoặc tâm trạng buồn bã.',
            'B': 'Chỉ định những yếu tố, chi tiết hoặc lỗi mà bạn KHÔNG MUỐN xuất hiện trong bức ảnh (ví dụ: ngón tay thừa, mờ nhòe, biến dạng).',
            'C': 'Giảm kích thước file ảnh để tải về nhanh hơn.',
            'D': 'Hủy bỏ lượt tạo ảnh ngay lập tức để tiết kiệm tín dụng (credit).'
        },
        'answer': 'B',
        'explanation': 'Negative Prompt là cơ chế mạnh mẽ cho phép người dùng liệt kê những đặc điểm muốn mô hình tránh tạo ra (ví dụ: blurry, distorted hands, extra limbs, low resolution, watermark), giúp chất lượng ảnh đầu ra đạt tiêu chuẩn cao hơn.'
    }
]

# Combine all
all_final = standardized_ebook + mock_questions + extra_questions
print(f"Total questions compiled: {len(all_final)}")
print(f"- From E-book: {len(standardized_ebook)}")
print(f"- From Mock Exam: {len(mock_questions)}")
print(f"- Synthesized High-Yield: {len(extra_questions)}")

# Check domain distribution
d_counts = {}
for q in all_final:
    d_counts[q['domain_id']] = d_counts.get(q['domain_id'], 0) + 1
print('Domain counts:', d_counts)

# Check type distribution
t_counts = {}
for q in all_final:
    t_counts[q['type']] = t_counts.get(q['type'], 0) + 1
print('Type counts:', t_counts)

with open('questions_db.json', 'w', encoding='utf-8') as f_out:
    json.dump(all_final, f_out, ensure_ascii=False, indent=2)

print('Successfully written questions_db.json!')
