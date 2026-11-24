import json
import pypdf
import os

print("Building comprehensive Theory Library from 4 PDF files...")

# 1. Gen AI - Bài tập Thực hành và Bài tập Dự án (15 pages)
r_bt = pypdf.PdfReader('Gen AI - Bài tập Thực hành và Bài tập Dự án.pdf')
practical_exercises_data = []

current_lesson = None
for page_idx, page in enumerate(r_bt.pages):
    txt = page.extract_text() or ''
    lines = txt.split('\n')
    for line in lines:
        line_clean = line.strip()
        if line_clean.startswith('BÀI ') and ':' in line_clean:
            current_lesson = {
                'page': page_idx + 1,
                'lesson_title': line_clean,
                'exercises': []
            }
            practical_exercises_data.append(current_lesson)
        elif line_clean.startswith('Bài tập ') and current_lesson:
            current_lesson['exercises'].append({
                'title': line_clean,
                'content': ''
            })

print(f"Extracted {len(practical_exercises_data)} lessons from Practical Exercises PDF")

# Compile detailed summaries for the 4 theoretical documents
theory_docs = {
    "doc1_ebook": {
        "title": "E-book Nền Tảng AI Tạo Sinh (99 trang)",
        "source": "E-book_Generative AI Foundation.pdf",
        "description": "Giáo trình nền tảng chính thức do IIG Vietnam biên soạn, bao quát toàn diện 19 bài học chia thành 4 Domain năng lực chuẩn quốc tế.",
        "domains": [
            {
                "id": 1,
                "name": "Domain 1: Các phương pháp và mô hình của AI tạo sinh",
                "lessons": [
                    {
                        "num": 1,
                        "title": "Định nghĩa AI tạo sinh",
                        "summary": "AI tạo sinh (Generative AI) là nhánh trí tuệ nhân tạo có khả năng tạo ra nội dung mới độc đáo (văn bản, ảnh, âm thanh, video, code) từ các gợi ý (prompts) dựa trên mẫu học từ dữ liệu lớn.",
                        "diff": "Khác biệt với Predictive AI (dự báo giá trị tương lai), Discriminative AI (phân loại nhãn) và Search Engine (tìm kiếm liên kết đến nội dung có sẵn).",
                        "exam_pointer": "Đề thi hay bẫy câu hỏi: khi nào dùng Search Engine vs khi nào dùng Gen AI; phân biệt 4 loại AI."
                    },
                    {
                        "num": 2,
                        "title": "Các quy trình của AI tạo sinh",
                        "summary": "Huấn luyện trước (Pre-training) bằng học không giám sát trên hàng nghìn tỷ token. Gán nhãn thủ công (Data Labeling) cho hình ảnh.",
                        "diff": "Mô hình ngôn ngữ doanh nghiệp (Enterprise LLMs) dùng dữ liệu nhỏ hơn nhưng cần chính xác; mô hình cộng đồng cần GPU/TPU khổng lồ.",
                        "exam_pointer": "Đặc biệt chú ý câu hỏi về lý do GPU vượt trội CPU (xử lý song song ma trận)."
                    },
                    {
                        "num": 3,
                        "title": "Các loại mô hình và thuật ngữ",
                        "summary": "Transformer (Attention mechanism, nền tảng LLM), CNN (tích chập, phân loại ảnh), Diffusion (khử nhiễu ngẫu nhiên tạo ảnh), GAN (mạng đối nghịch Generator - Discriminator), VAE (bộ tự mã hóa biến phân, phát hiện dị thường).",
                        "diff": "Siêu tham số (Hyperparameters): Temperature (nhiệt độ ngẫu nhiên), Top-P (lấy mẫu hạt nhân), Max Tokens (độ dài).",
                        "exam_pointer": "Kéo thả định nghĩa: Token, Dataset, Neural Network, CNN; cơ chế mô hình Diffusion tạo ảnh từ nhiễu."
                    },
                    {
                        "num": 4,
                        "title": "Các loại đầu vào, đầu ra và nhiệm vụ",
                        "summary": "Đa dạng hóa đầu vào cho một đầu ra (Multimodal). Văn bản → Văn bản (ChatGPT), Văn bản → Ảnh (DALL-E, Midjourney), Văn bản → Giọng nói (ElevenLabs), Văn bản → Video (Sora, InVideo).",
                        "diff": "Ứng dụng độc lập (Standalone AI Apps) như Microsoft Copilot tích hợp sẵn chức năng tối ưu hóa công việc.",
                        "exam_pointer": "Bảng Đúng/Sai về các loại đầu vào và đầu ra của công cụ AI."
                    },
                    {
                        "num": 5,
                        "title": "Chọn một công cụ cho một nhiệm vụ",
                        "summary": "Tiêu chí lựa chọn: mục đích chuyên biệt, khả năng tùy biến, chi phí / tín dụng miễn phí, và độ bảo mật quyền riêng tư.",
                        "diff": "Ví dụ: Stable Diffusion cho tùy biến cao; Canva/Copilot cho tác vụ văn phòng nhanh.",
                        "exam_pointer": "Tình huống chọn công cụ phù hợp với ngân sách và yêu cầu doanh nghiệp."
                    },
                    {
                        "num": 6,
                        "title": "Những hạn chế của AI tạo sinh",
                        "summary": "Ảo giác (Hallucination - tự tin bịa thông tin sai), độ trễ thời gian (mốc cut-off kiến thức), tính nhất quán thấp khi temperature cao, thiên lệch dữ liệu (Bias).",
                        "diff": "Ảo giác không phụ thuộc vào văn phong; văn phong càng trôi chảy càng dễ làm người dùng tin nhầm.",
                        "exam_pointer": "Bẫy đề thi: Văn phong trôi chảy không đồng nghĩa với đáng tin cậy."
                    }
                ]
            },
            {
                "id": 2,
                "name": "Domain 2: Kỹ thuật xây dựng câu lệnh (Prompt Engineering) cơ bản",
                "lessons": [
                    {
                        "num": 7,
                        "title": "Xác định câu lệnh (Prompt Fundamentals)",
                        "summary": "Cấu trúc 4 thành phần: Role (Vai trò), Task (Nhiệm vụ), Context (Ngữ cảnh), Format/Constraints (Định dạng & Ràng buộc).",
                        "diff": "Gán vai trò Persona giúp AI định hình kiến thức chuyên ngành và văn phong phù hợp.",
                        "exam_pointer": "Đề thi hay yêu cầu chọn câu prompt hiệu quả nhất có đủ 4 thành phần."
                    },
                    {
                        "num": 8,
                        "title": "Câu lệnh để chuyển đổi nội dung (Transform Content)",
                        "summary": "Tóm tắt văn bản, dịch thuật đa ngôn ngữ, chuyển đổi văn bản thành bảng so sánh 3 cột, trích xuất thông tin cấu trúc (JSON).",
                        "diff": "Phân biệt chuyển đổi nội dung với sáng tạo ý tưởng mới (Ideation).",
                        "exam_pointer": "Chọn 2 prompt thuộc nhóm chuyển đổi nội dung."
                    },
                    {
                        "num": 9,
                        "title": "Câu lệnh liên quan đến hình ảnh (Image Prompts)",
                        "summary": "Cấu trúc: Chủ thể chính + Hành động + Bối cảnh + Phong cách nghệ thuật (màu nước, cyberpunk, 3D) + Ánh sáng + Tỷ lệ khung hình (--ar 16:9).",
                        "diff": "Negative Prompt: loại bỏ các chi tiết không mong muốn (mờ nhòe, biến dạng bàn tay).",
                        "exam_pointer": "Kéo thả các cụm từ trong prompt vào đúng vai trò thành phần."
                    },
                    {
                        "num": 10,
                        "title": "Câu lệnh liên quan đến video (Video Prompts)",
                        "summary": "Chuyển động camera (pan, zoom, tilt), nội suy khung hình (interpolation làm mượt), avatar thuyết trình và giới hạn tín dụng.",
                        "diff": "Công cụ: InVideo AI, Runway Gen-2, Elai.io.",
                        "exam_pointer": "Định nghĩa nội suy khung hình và avatar ảo."
                    }
                ]
            },
            {
                "id": 3,
                "name": "Domain 3: Tinh chỉnh câu lệnh (Prompt Refinement)",
                "lessons": [
                    {
                        "num": 11,
                        "title": "Cải thiện câu lệnh (Refinement Process)",
                        "summary": "Quy trình lặp lại (Iterative refinement): viết prompt ban đầu -> đọc đánh giá -> tinh chỉnh thêm ngữ cảnh/ràng buộc -> kiểm chứng kết quả.",
                        "diff": "Tận dụng lịch sử trò chuyện trong cùng phiên thay vì bắt đầu lại từ đầu.",
                        "exam_pointer": "Sắp xếp đúng 5 bước làm việc với AI tạo sinh."
                    },
                    {
                        "num": 12,
                        "title": "Thêm đầu vào vào câu lệnh (Context & Delimiters)",
                        "summary": "Sử dụng ký tự phân cách (Delimiters như \"\"\", ---, XML tags) để ngăn nhầm lẫn giữa câu lệnh và tài liệu. Cung cấp bảng thuật ngữ (Glossary) khi dịch.",
                        "diff": "Cung cấp ví dụ Few-shot để AI làm đúng định dạng mong muốn.",
                        "exam_pointer": "Kỹ thuật giúp thuật ngữ chuyên ngành dịch nhất quán nhất là dùng Glossary."
                    },
                    {
                        "num": 13,
                        "title": "Các kỹ thuật gợi ý nâng cao",
                        "summary": "Zero-shot (không ví dụ), Few-shot (kèm ví dụ có nhãn), Chain-of-Thought (hãy suy luận từng bước), Generated Knowledge (tạo tri thức trước rồi viết bài), Reverse Prompting (đưa ảnh/bài mẫu nhờ AI viết prompt).",
                        "diff": "CoT tăng mạnh độ chính xác cho bài toán logic và số học.",
                        "exam_pointer": "Kéo thả nhận diện ví dụ của từng kỹ thuật prompt."
                    },
                    {
                        "num": 14,
                        "title": "Xác minh độ chính xác (Fact-Checking)",
                        "summary": "Kiểm tra dữ liệu lịch sử (AI hay thiếu các sự kiện mới nhất), kiểm tra số liệu tính toán (tự tính lại bằng máy tính), đối chiếu nguồn độc lập.",
                        "diff": "LLM dự đoán từ tiếp theo chứ không làm toán chính xác.",
                        "exam_pointer": "Phải tự kiểm tra lại diện tích, doanh thu, tỷ lệ % do AI đưa ra."
                    },
                    {
                        "num": 15,
                        "title": "Kiểm tra tính nhất quán (Consistency)",
                        "summary": "Chạy lặp lại câu lệnh trong phiên mới để đo độ phân tán kết quả. Đặt temperature thấp để tăng nhất quán.",
                        "diff": "Self-consistency: sinh nhiều luồng suy luận rồi lấy đáp án đa số.",
                        "exam_pointer": "Đúng/Sai về tính nhất quán giữa các lần hỏi."
                    },
                    {
                        "num": 16,
                        "title": "Chuỗi câu lệnh (Prompt Chaining)",
                        "summary": "Chia bài toán lớn thành chuỗi các bước nhỏ: Output của bước 1 làm Input cho bước 2.",
                        "diff": "Kiểm soát sai số, giảm tải độ phức tạp nhận thức của mô hình.",
                        "exam_pointer": "Nhận diện sơ đồ Prompt Chaining trong đề thi hình ảnh."
                    }
                ]
            },
            {
                "id": 4,
                "name": "Domain 4: Đạo đức, pháp luật và tác động xã hội của AI",
                "lessons": [
                    {
                        "num": 17,
                        "title": "Bản quyền & Quyền riêng tư dữ liệu (PII)",
                        "summary": "Tác phẩm hoàn toàn do AI tạo sinh KHÔNG được cấp bản quyền vì thiếu tính sáng tạo con người (Human authorship).",
                        "diff": "PII (CCCD, tài khoản ngân hàng, bệnh án) tuyệt đối không đưa lên chatbot công cộng.",
                        "exam_pointer": "Quy định bản quyền tác giả và bảo vệ thông tin định danh cá nhân."
                    },
                    {
                        "num": 18,
                        "title": "Rủi ro của Trí tuệ nhân tạo tạo sinh",
                        "summary": "Deepfake giả mạo giọng nói/khuôn mặt lừa đảo, email phishing tinh vi, rò rỉ bí mật thương mại, nhiễm độc dữ liệu (Data poisoning).",
                        "diff": "Người dùng phải chịu trách nhiệm cá nhân về nội dung AI do mình xuất bản.",
                        "exam_pointer": "Hậu quả pháp lý khi để lộ dữ liệu khách hàng hoặc phát tán deepfake."
                    },
                    {
                        "num": 19,
                        "title": "Tác động xã hội & Sử dụng AI có trách nhiệm",
                        "summary": "Mặt tích cực: Tăng năng suất, hỗ trợ người khuyết tật. Mặt tiêu cực: Giảm tương tác trực tiếp, tiêu tốn năng lượng và nước làm mát trung tâm dữ liệu.",
                        "diff": "Nguyên tắc Responsible AI: Minh bạch (Transparency), Công bằng (Fairness), Trách nhiệm giải trình có con người giám sát (Accountability).",
                        "exam_pointer": "Chọn 3 nguyên tắc bắt buộc của Responsible AI."
                    }
                ]
            }
        ]
    },
    "doc2_practical": {
        "title": "Gen AI - Bài Tập Thực Hành & Bài Tập Dự Án (15 trang)",
        "source": "Gen AI - Bài tập Thực hành và Bài tập Dự án.pdf",
        "description": "Tập hợp các bài thực hành thực chiến trên ChatGPT, Gemini, Canva AI, Midjourney, InVideo từ Bài 1 đến Bài 19 và Dự án hoàn chỉnh.",
        "projects_overview": [
            {
                "lesson": "Bài 1 - 3: Khám phá & Huấn luyện",
                "tasks": [
                    "Thực hành 1: Yêu cầu ChatGPT tóm tắt khóa học AI tạo sinh + vẽ mindmap dạng text.",
                    "Thực hành 2: Hỏi ChatGPT về sự kiện thực tế rồi tra Google/Wikipedia để đối chiếu ảo giác.",
                    "Thực hành 3: Thử nghiệm huấn luyện mô hình phân loại ảnh với Teachable Machine / Google Colab (thay đổi epochs, batch size, quan sát GPU)."
                ]
            },
            {
                "lesson": "Bài 4 - 6: Đa phương thức & Hạn chế",
                "tasks": [
                    "Thực hành 1: Thử nghiệm Text-to-Text, Text-to-Image (Canva AI / DALL-E), Text-to-Audio (ElevenLabs).",
                    "Thực hành 2: Đánh giá so sánh 2 công cụ cho cùng 1 tác vụ marketing thiết bị thông minh.",
                    "Thực hành 3: Đặt các câu hỏi có bẫy thời gian thực để chứng kiến mốc cut-off kiến thức của mô hình."
                ]
            },
            {
                "lesson": "Bài 7 - 10: Thực hành Prompt chuyên biệt",
                "tasks": [
                    "Thực hành 1: Thu thập thông tin và tóm tắt bài báo khoa học dài cho học sinh lớp 10.",
                    "Thực hành 2: Chuyển đổi đoạn văn bản mô tả kỹ thuật thành bảng so sánh 3 cột.",
                    "Thực hành 3: Tạo hình ảnh thiết bị thông minh phòng khách bằng Midjourney/Canva với tỷ lệ 16:9, phong cách màu nước.",
                    "Thực hành 4: Tạo video 5 giây với avatar đọc bản tin trong InVideo AI / Elai.io."
                ]
            },
            {
                "lesson": "Bài 11 - 16: Tinh chỉnh & Kiểm chứng",
                "tasks": [
                    "Thực hành 1: Áp dụng Persona (chuyên gia marketing) và ràng buộc độ dài 150 chữ.",
                    "Thực hành 2: Cung cấp Glossary thuật ngữ tiếng Anh - Việt cho đoạn dịch hợp đồng.",
                    "Thực hành 3: Thực hành Chain-of-Thought giải bài toán tối ưu năng lượng nhà thông minh.",
                    "Thực hành 4: Thực hành Reverse Prompting: đưa bức ảnh mẫu và yêu cầu AI tái tạo câu prompt."
                ]
            },
            {
                "lesson": "Bài 17 - 19: Đạo đức & Dự án tổng kết",
                "tasks": [
                    "Thực hành 1: Nhận diện và làm sạch PII trong đoạn email giả lập trước khi nộp lên AI.",
                    "Thực hành 2: Phân tích email lừa đảo (phishing) và xây dựng checklist an toàn thông tin.",
                    "Dự án cuối khóa (Capstone Project): Xây dựng chiến dịch truyền thông đa phương tiện hoàn chỉnh cho sản phẩm Smart Thermostat bằng bộ công cụ AI tạo sinh."
                ]
            }
        ]
    },
    "doc3_teacher_guide": {
        "title": "Teacher Guide - Hướng Dẫn Giáo Viên (198 trang)",
        "source": "GEN AI TEACHER GUIDE.pdf",
        "description": "Tài liệu giảng dạy chuyên sâu bám sát mục tiêu bài thi Pearson - Certiport, tổng hợp phương pháp sư phạm, các điểm nhấn kiến thức và phân tích bẫy đề thi.",
        "key_sections": [
            {
                "title": "1. Ma trận mục tiêu bài thi Pearson - Certiport (Exam Objectives)",
                "content": "Bài thi Generative AI Foundations đánh giá 4 Domain: 1.0 Generative AI Methods (25%), 2.0 Basic Prompt Engineering (30%), 3.0 Prompt Refinement (25%), 4.0 Ethics, Legal and Social Impact (20%). Điểm đỗ là 700/1000."
            },
            {
                "title": "2. Phân tích bẫy câu hỏi nhiễu (Distractor Traps Analysis)",
                "content": "Teacher Guide chỉ rõ những chỗ học sinh dễ mất điểm nhất: Bẫy nhầm lẫn giữa AI tạo sinh và Công cụ tìm kiếm; Bẫy tin vào văn phong tự tin của mô hình bị ảo giác; Bẫy ngộ nhận bản quyền thuộc về người viết prompt; Bẫy coi prompt dài luôn tốt hơn prompt ngắn; Bẫy tính toán số học của LLM."
            },
            {
                "title": "3. Phương pháp giảng dạy 'Human-in-the-Loop'",
                "content": "Giáo viên luôn nhấn mạnh nguyên tắc: AI là trợ lý khuếch đại năng suất, con người là người kiểm chứng cuối cùng và chịu trách nhiệm pháp lý cao nhất."
            },
            {
                "title": "4. Kỹ thuật đánh giá và chấm điểm mô phỏng Gmetrix",
                "content": "Trong các câu hỏi phức hợp (chọn nhiều đáp án, bảng Đúng/Sai 4 ý, sắp xếp thứ tự, kéo thả), học sinh PHẢI ĐÚNG 100% TẤT CẢ CÁC Ý MỚI ĐƯỢC 25 ĐIỂM. Không có điểm thành phần từng ý."
            }
        ]
    },
    "doc4_practice_exercises": {
        "title": "Practice Exercises Chuyên Sâu (127 trang)",
        "source": "Generative AI Foundation Practice Exercises 1 (1).pdf",
        "description": "Hệ thống bài tập tình huống thực tế chuyên sâu bám sát từng mục tiêu exam objective, kèm rubric đánh giá và bài giải mẫu.",
        "core_skills": [
            {
                "skill": "Xác minh thông tin hiện tại & Số liệu",
                "detail": "Kỹ thuật kiểm chứng số liệu tài chính, diện tích, giá cổ phiếu bằng các truy vấn độc lập và bảng tính."
            },
            {
                "skill": "Phát hiện dấu hiệu 'Nghe hợp lý nhưng chưa chắc đúng'",
                "detail": "Rèn luyện phản xạ nhận diện ảo giác (hallucination indicators) trong văn bản y tế, kỹ thuật, pháp lý."
            },
            {
                "skill": "Tối ưu hóa Prompt theo tiêu chí Mục đích - Chi phí - Quyền riêng tư",
                "detail": "Lập bảng ma trận so sánh chi phí API, giới hạn rate limit và chính sách lưu trữ dữ liệu của các nhà cung cấp AI lớn."
            },
            {
                "skill": "Xây dựng Checklist rủi ro trước khi công bố sản phẩm AI",
                "detail": "Quy trình kiểm duyệt 5 bước: Kiểm tra PII -> Kiểm tra bản quyền hình ảnh -> Kiểm tra độ chính xác sự thật -> Rà soát thiên kiến -> Ghi nhận nguồn gốc minh bạch."
            }
        ]
    }
}

js_content = 'const THEORY_DOCS = ' + json.dumps(theory_docs, ensure_ascii=False, indent=2) + ';\n'
with open('theory_library.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Generated theory_library.js successfully ({len(js_content)} bytes)")
