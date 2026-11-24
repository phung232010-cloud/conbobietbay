import json

study_guide = [
    {
        "domain_id": 1,
        "domain_name": "Các phương pháp và mô hình Generative AI",
        "description": "Nắm vững bản chất của AI tạo sinh, phân biệt với các loại AI khác, các kiến trúc mô hình (Transformer, CNN, Diffusion, GAN, VAE), quy trình huấn luyện và siêu tham số.",
        "lessons": [
            {
                "id": 1,
                "title": "Định nghĩa AI tạo sinh",
                "key_points": [
                    "AI tạo sinh (Generative AI) sinh ra nội dung MỚI (văn bản, hình ảnh, âm thanh, video, mã nguồn) dựa trên dữ liệu đã học.",
                    "Phân biệt: Predictive AI (dự báo giá trị tương lai), Discriminative/Analytical AI (phân loại, gán nhãn, phát hiện spam), Statistical AI (thống kê toán học, phương sai, hồi quy).",
                    "So sánh với Search Engine: Công cụ tìm kiếm tìm và liên kết đến thông tin CÓ SẴN; AI tạo sinh TỔNG HỢP và SINH NỘI DUNG MỚI theo yêu cầu bằng ngôn ngữ tự nhiên.",
                    "Khóa học gồm 4 Domain cốt lõi: 1) Phương pháp và mô hình, 2) Kỹ thuật Prompt cơ bản, 3) Tinh chỉnh Prompt & Đánh giá, 4) Đạo đức, pháp luật & Xã hội."
                ]
            },
            {
                "id": 2,
                "title": "Các quy trình của AI tạo sinh & Phần cứng",
                "key_points": [
                    "Huấn luyện trước (Pre-training): Học không giám sát trên lượng dữ liệu khổng lồ hàng nghìn tỷ token để dự đoán từ tiếp theo.",
                    "Dữ liệu huấn luyện: Quy mô lớn, đa dạng; dữ liệu nội bộ doanh nghiệp có thể nhỏ hơn nhưng cần độ chính xác cao.",
                    "Gán nhãn thủ công (Data Labeling): Cần thiết cho các mô hình hình ảnh và học có giám sát để liên kết từ khóa với đặc trưng hình ảnh.",
                    "Phần cứng: GPU (Graphics Processing Unit) và TPU (Tensor Processing Unit) vượt trội hoàn toàn so với CPU nhờ kiến trúc tính toán song song hàng nghìn lõi tối ưu cho phép nhân ma trận."
                ]
            },
            {
                "id": 3,
                "title": "Các loại mô hình và thuật ngữ cốt lõi",
                "key_points": [
                    "Transformer: Kiến trúc đột phá với cơ chế Tự chú ý (Self-Attention), nền tảng của GPT, Claude, Gemini, LLaMA.",
                    "CNN (Mạng nơ-ron tích chập): Chuyên xử lý và phân loại hình ảnh bằng các bộ lọc quét vùng.",
                    "Diffusion Model: Khử nhiễu ngẫu nhiên (denoising) từng bước để tạo ra hình ảnh chất lượng cao (Midjourney, Stable Diffusion, DALL-E 3).",
                    "GAN (Generative Adversarial Network): Gồm 2 mạng Đối nghịch nhau — Bộ tạo (Generator) và Bộ phân biệt (Discriminator).",
                    "VAE (Variational Autoencoder): Bộ tự mã hóa biến phân, hiệu quả cao trong phát hiện dị thường dữ liệu (anomaly detection).",
                    "Token: Đơn vị văn bản nhỏ nhất (từ, cụm ký tự, dấu câu) mà LLM phân tích và sinh ra.",
                    "Siêu tham số (Hyperparameters): Thiết lập trước khi chạy — Temperature (độ ngẫu nhiên), Top-P (lấy mẫu tích lũy), Max Tokens (độ dài tối đa)."
                ]
            },
            {
                "id": 4,
                "title": "Đa dạng đầu vào, đầu ra & Tác vụ AI",
                "key_points": [
                    "Đa phương thức (Multimodal): Mô hình nhận nhiều loại đầu vào (văn bản + ảnh + âm thanh) để cho một đầu ra tối ưu.",
                    "Text-to-Text (ChatGPT, Claude), Text-to-Image (DALL-E, Midjourney), Text-to-Audio (ElevenLabs, Suno), Text-to-Video (Sora, Runway, InVideo).",
                    "Ứng dụng độc lập (Standalone AI Apps): Tích hợp sẵn chức năng hoàn chỉnh cho người dùng văn phòng (Microsoft Copilot, Canva Magic Studio)."
                ]
            },
            {
                "id": 5,
                "title": "Lựa chọn công cụ cho một nhiệm vụ",
                "key_points": [
                    "Đánh giá công cụ theo 4 tiêu chuẩn: Mục đích sử dụng, Khả năng tùy biến, Chi phí/Giới hạn tín dụng, và Độ bảo mật riêng tư.",
                    "Ví dụ: Stable Diffusion phù hợp tạo ảnh tùy biến sâu; GitHub Copilot hỗ trợ lập trình; InVideo tạo clip nhanh."
                ]
            },
            {
                "id": 6,
                "title": "Những hạn chế của AI tạo sinh",
                "key_points": [
                    "Ảo giác (Hallucination): Tự tin tạo ra thông tin nghe rất thuyết phục nhưng sai sự thật hoặc không hề tồn tại.",
                    "Độ trễ thời gian (Knowledge Cut-off): Mô hình không tự động cập nhật tin tức tức thời trừ khi kết nối công cụ tìm kiếm hoặc RAG.",
                    "Kém nhất quán: Cùng một prompt hỏi hai lần có thể ra hai câu trả lời khác nhau nếu temperature > 0.",
                    "Thiên lệch (Bias): Phản ánh lại các định kiến có trong dữ liệu huấn luyện Internet."
                ]
            }
        ]
    },
    {
        "domain_id": 2,
        "domain_name": "Kỹ thuật xây dựng Prompt cơ bản",
        "description": "Các kỹ thuật thiết lập câu lệnh rõ ràng, gán vai trò, cấu trúc prompt chuyển đổi nội dung, thiết kế prompt hình ảnh và video.",
        "lessons": [
            {
                "id": 7,
                "title": "Xác định câu lệnh (Prompt Fundamentals)",
                "key_points": [
                    "4 thành phần chuẩn của một Prompt: Role (Vai trò), Task (Nhiệm vụ), Context (Ngữ cảnh), Format/Constraints (Định dạng & Ràng buộc).",
                    "Gán vai trò (Persona): Giúp AI định hình văn phong, chuyên môn và góc nhìn phù hợp (ví dụ: 'Bạn là chuyên gia dinh dưỡng...').",
                    "Ràng buộc rõ ràng: Chỉ định độ dài (dưới 200 từ), gạch đầu dòng, bảng biểu, tránh viết tắt."
                ]
            },
            {
                "id": 8,
                "title": "Câu lệnh chuyển đổi nội dung (Transform Content)",
                "key_points": [
                    "Chuyển đổi nội dung: Tóm tắt bài báo, dịch thuật đa ngữ, chuyển văn bản thành bảng so sánh, trích xuất dữ liệu có cấu trúc (JSON).",
                    "Khác với tạo mới ý tưởng (Ideation) hoặc truy vấn thông tin đơn thuần."
                ]
            },
            {
                "id": 9,
                "title": "Câu lệnh hình ảnh (Image Prompting)",
                "key_points": [
                    "Cấu trúc prompt tạo ảnh: Chủ thể chính + Hành động + Bối cảnh/Địa điểm + Phong cách nghệ thuật (màu nước, sơn dầu, 3D render) + Ánh sáng (chiều tà, cinematic) + Góc máy + Tỷ lệ khung hình (--ar 16:9, 1:1).",
                    "Negative Prompt: Liệt kê các chi tiết KHÔNG muốn xuất hiện (blurry, bad anatomy, watermark, text) để nâng cao chất lượng ảnh."
                ]
            },
            {
                "id": 10,
                "title": "Câu lệnh video (Video Prompting)",
                "key_points": [
                    "Quy định chuyển động camera: Pan (lia ngang), Zoom in/out, Drone shot, Static camera.",
                    "Nội suy khung hình (Interpolation): Thêm khung hình trung gian để video mượt mà, giảm giật lag.",
                    "Avatar ảo (AI Avatar): Gán kịch bản thuyết trình và biểu cảm khuôn mặt."
                ]
            }
        ]
    },
    {
        "domain_id": 3,
        "domain_name": "Tinh chỉnh Prompt & Đánh giá mô hình",
        "description": "Nâng cấp prompt từ cơ bản lên chuyên nghiệp: Zero-shot, Few-shot, Chain-of-Thought, Generated Knowledge, Reverse Prompting, Prompt Chaining và kiểm chứng thông tin.",
        "lessons": [
            {
                "id": 11,
                "title": "Cải thiện câu lệnh (Prompt Refinement)",
                "key_points": [
                    "Quy trình lặp lại (Iterative Refinement): Đưa prompt ban đầu -> Đánh giá kết quả -> Thêm chi tiết, điều chỉnh văn phong -> Kiểm tra lại.",
                    "Sử dụng bộ nhớ ngữ cảnh trong cùng phiên trò chuyện để tinh chỉnh dần mà không cần viết lại từ đầu."
                ]
            },
            {
                "id": 12,
                "title": "Thêm đầu vào vào câu lệnh (Context & Delimiters)",
                "key_points": [
                    "Ký tự phân cách (Delimiters): Dùng \"\"\", ---, hoặc thẻ XML (<context>...</context>) để tách biệt chỉ dẫn và dữ liệu tài liệu.",
                    "Bảng thuật ngữ (Glossary): Đính kèm danh sách thuật ngữ chuyên ngành để đảm bảo tính nhất quán khi dịch thuật hoặc phân tích."
                ]
            },
            {
                "id": 13,
                "title": "Các kỹ thuật Prompt phổ biến & Nâng cao",
                "key_points": [
                    "Zero-shot: Yêu cầu AI làm việc ngay mà không đưa ví dụ mẫu nào.",
                    "Few-shot: Đưa ra một vài cặp ví dụ mẫu (Đầu vào -> Đầu ra mong muốn) trước khi hỏi để AI bắt chước đúng định dạng.",
                    "Chain-of-Thought (CoT): Yêu cầu AI 'Hãy suy luận từng bước' (Step-by-step reasoning), giải quyết bài toán logic và số học hiệu quả.",
                    "Generated Knowledge: Yêu cầu AI sinh ra các sự thật liên quan trước rồi dùng chính các sự thật đó để hoàn thành bài viết.",
                    "Reverse Prompting (Prompt ngược): Đưa sản phẩm mẫu cho AI và yêu cầu AI viết ra câu prompt có thể tạo ra sản phẩm đó."
                ]
            },
            {
                "id": 14,
                "title": "Xác minh thông tin từ AI (Fact-Checking)",
                "key_points": [
                    "Kiểm tra dữ liệu lịch sử: AI có thể nhầm lẫn mốc thời gian hoặc thiếu phiên bản mới.",
                    "Kiểm tra số liệu toán học: AI thường tính toán sai do cơ chế xác suất chữ tiếp theo -> Luôn tự tính lại bằng máy tính.",
                    "Kiểm tra chéo (Cross-check) với các nguồn dữ liệu chính thống bên ngoài."
                ]
            },
            {
                "id": 15,
                "title": "Kiểm tra tính nhất quán (Consistency)",
                "key_points": [
                    "Thử nghiệm lại câu lệnh nhiều lần trong cửa sổ mới để kiểm tra tính ổn định.",
                    "Kỹ thuật Self-consistency: Lấy kết quả xuất hiện nhiều nhất từ nhiều lần suy luận."
                ]
            },
            {
                "id": 16,
                "title": "Chuỗi câu lệnh (Prompt Chaining)",
                "key_points": [
                    "Phân tách một bài toán lớn, phức tạp thành chuỗi các bước tuần tự liên tiếp.",
                    "Đầu ra của Bước 1 (Output 1) được xử lý làm đầu vào cho Bước 2 (Input 2), giúp kiểm soát chất lượng chặt chẽ ở từng công đoạn."
                ]
            }
        ]
    },
    {
        "domain_id": 4,
        "domain_name": "Đạo đức, Pháp luật & Tác động xã hội",
        "description": "Bản quyền trí tuệ, quyền riêng tư dữ liệu (PII), deepfake, tấn công lừa đảo, thiên lệch định kiến và nguyên tắc AI có trách nhiệm.",
        "lessons": [
            {
                "id": 17,
                "title": "Bản quyền, Pháp lý & Quyền riêng tư",
                "key_points": [
                    "Bản quyền (Copyright): Tác phẩm hoàn toàn do AI tạo ra KHÔNG được cấp bản quyền vì bản quyền chỉ bảo hộ sáng tạo của con người.",
                    "Sử dụng hợp lý (Fair Use): Tranh cãi pháp lý về việc các công ty AI sử dụng tác phẩm có bản quyền trên mạng để huấn luyện mô hình.",
                    "Bảo vệ PII (Thông tin định danh cá nhân): Tuyệt đối không nhập CCCD, tài khoản ngân hàng, hồ sơ bệnh án, mật khẩu lên chatbot AI công cộng."
                ]
            },
            {
                "id": 18,
                "title": "Rủi ro của Trí tuệ nhân tạo tạo sinh",
                "key_points": [
                    "Deepfake: Giả mạo giọng nói, khuôn mặt của lãnh đạo hoặc người thân để lừa đảo chuyển tiền hoặc bôi nhọ danh dự.",
                    "Tấn công lừa đảo (Phishing): Kẻ xấu dùng AI soạn email giả mạo tinh vi, chuẩn ngữ pháp, khó phát hiện.",
                    "Rò rỉ dữ liệu doanh nghiệp: Nhân viên dán mã nguồn nội bộ hoặc chiến lược mật lên công cụ AI bên ngoài.",
                    "Data Poisoning (Nhiễm độc dữ liệu): Kẻ tấn công can thiệp vào tập dữ liệu huấn luyện để gây sai lệch mô hình."
                ]
            },
            {
                "id": 19,
                "title": "Tác động xã hội & Sử dụng AI có trách nhiệm",
                "key_points": [
                    "Tác động tích cực: Tăng năng suất lao động, phá vỡ rào cản ngôn ngữ, hỗ trợ cá nhân hóa học tập và người khuyết tật.",
                    "Tác động tiêu cực: Nguy cơ mất việc làm các ngành sáng tạo/viết lách, giảm tương tác con người, tiêu thụ lượng điện và nước làm mát máy chủ khổng lồ.",
                    "Trụ cột Responsible AI: Minh bạch (Transparency - thông báo khi dùng AI), Công bằng (Fairness - giảm thiên kiến), Trách nhiệm giải trình (Accountability - con người luôn chịu trách nhiệm cuối cùng)."
                ]
            }
        ]
    }
]

traps_guide = [
    {
        "trap_id": 1,
        "title": "Bẫy Phân biệt AI tạo sinh vs Công cụ tìm kiếm (Search Engine)",
        "trap_content": "Đề thi hay hỏi: 'Khi cần tìm tài liệu tham khảo chính xác kèm liên kết web thì dùng gì?'.",
        "mistake": "Nhiều bạn chọn Chatbot AI tạo sinh vì nghĩ AI biết hết.",
        "correct_rule": "Công cụ tìm kiếm (Google, Bing) trả về liên kết trang web có sẵn. AI tạo sinh dùng khi cần TẠO RA nội dung mới (soạn email, lập dàn ý, viết code, tạo kịch bản)."
    },
    {
        "trap_id": 2,
        "title": "Bẫy Ảo giác vs Văn phong trôi chảy tự tin",
        "trap_content": "Đề thi hỏi: 'Nội dung AI viết nghe rất trôi chảy, thuyết phục và đầy đủ số liệu thì có luôn đúng không?'.",
        "mistake": "Học sinh chọn Đúng vì thấy văn phong quá hoàn hảo và có trích dẫn tác giả.",
        "correct_rule": "Ảo giác (Hallucination) là hiện tượng AI bịa thông tin một cách cực kỳ tự tin và trôi chảy. Phải luôn kiểm chứng chéo số liệu và nguồn tin."
    },
    {
        "trap_id": 3,
        "title": "Bẫy Bản quyền tác phẩm AI (Copyright)",
        "trap_content": "Đề thi hỏi: 'Một bức ảnh do AI vẽ hoàn toàn từ câu prompt ngắn có được cấp bản quyền tác giả không? Thuộc về ai?'.",
        "mistake": "Nhiều bạn chọn 'Thuộc bản quyền của người gõ prompt' hoặc 'Thuộc công ty AI'.",
        "correct_rule": "Luật bản quyền (như USCO) chỉ bảo hộ sáng tạo của CON NGƯỜI (Human authorship). Tác phẩm hoàn toàn do AI sinh ra không có bản quyền."
    },
    {
        "trap_id": 4,
        "title": "Bẫy Phân biệt Few-shot vs Zero-shot vs Chain-of-Thought",
        "trap_content": "Nhầm lẫn giữa các kỹ thuật trong câu hỏi tình huống hoặc kéo thả.",
        "mistake": "Nhầm câu lệnh có ví dụ (Few-shot) với câu lệnh suy luận từng bước (Chain-of-thought).",
        "correct_rule": "Zero-shot: KHÔNG có ví dụ nào. Few-shot: Có 1-3 CẶP VÍ DỤ mẫu (Input -> Output). Chain-of-thought: 'Hãy suy luận từng bước' (Step-by-step)."
    },
    {
        "trap_id": 5,
        "title": "Bẫy Prompt dài vs Prompt hiệu quả",
        "trap_content": "Đề thi hỏi Đúng/Sai: 'Prompt càng dài thì kết quả chắc chắn càng tốt?'.",
        "mistake": "Chọn Đúng vì nghĩ càng nhiều chữ AI càng hiểu.",
        "correct_rule": "SAI. Prompt dài nhưng lan man, mâu thuẫn, nhiều từ viết tắt sẽ làm AI bối rối và sinh kết quả kém. Prompt tốt cần: Rõ ràng, cụ thể, đủ ngữ cảnh và ràng buộc."
    },
    {
        "trap_id": 6,
        "title": "Bẫy Đánh giá kết quả số học và tính toán của LLM",
        "trap_content": "Hỏi về cách xử lý số liệu diện tích, phần trăm, doanh thu do AI tính.",
        "mistake": "Nhiều bạn tin tưởng AI tính nhẩm giỏi hơn con người.",
        "correct_rule": "LLM là mô hình dự đoán từ tiếp theo theo xác suất, không phải máy tính số học. Luôn phải tính lại bằng máy tính cầm tay hoặc bảng tính độc lập."
    },
    {
        "trap_id": 7,
        "title": "Bẫy Quy chế chấm điểm thi Gmetrix / AI or Behind",
        "trap_content": "Đề thi gồm 40 câu / 50 phút / 1000 điểm. Mỗi câu 25 điểm.",
        "mistake": "Nghĩ rằng câu Đúng/Sai hoặc Chọn nhiều được điểm từng phần (partial credit).",
        "correct_rule": "Trong thi thật, câu có nhiều ý (chọn nhiều, Đúng/Sai cả 4 ý a,b,c,d, sắp xếp, ghép nối) CHỈ ĐƯỢC ĐIỂM KHI LÀM ĐÚNG 100% TOÀN BỘ CÁC Ý. Sai 1 ý là mất trọn 25 điểm câu đó!"
    }
]

js_content = 'const STUDY_GUIDE = ' + json.dumps(study_guide, ensure_ascii=False, indent=2) + ';\n'
js_content += 'const TRAPS_GUIDE = ' + json.dumps(traps_guide, ensure_ascii=False, indent=2) + ';\n'

with open('study_notes.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print('Generated study_notes.js successfully!')
