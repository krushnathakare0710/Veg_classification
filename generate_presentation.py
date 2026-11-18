import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]  # Blank slide

    # Theme Colors (Professional White & Emerald Theme)
    BG_COLOR = RGBColor(248, 250, 252)        # Slate 50
    CARD_BG = RGBColor(255, 255, 255)         # Pure White
    CARD_BORDER = RGBColor(226, 232, 240)     # Slate 200
    TEXT_MAIN = RGBColor(15, 23, 42)          # Slate 900
    TEXT_MUTED = RGBColor(71, 85, 105)        # Slate 600
    TEXT_LIGHT = RGBColor(148, 163, 184)      # Slate 400
    ACCENT_EMERALD = RGBColor(5, 150, 105)    # Emerald 600
    ACCENT_LIGHT = RGBColor(236, 253, 245)    # Emerald 50
    ACCENT_BORDER = RGBColor(167, 243, 208)   # Emerald 200

    FONT_FAMILY = "Segoe UI"

    def apply_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.color.rgb = BG_COLOR

    def add_footer(slide, slide_num):
        # Footer rule line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = CARD_BORDER
        line.line.color.rgb = CARD_BORDER

        # Footer text
        tx = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(8.0), Inches(0.35))
        tf = tx.text_frame
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        p = tf.paragraphs[0]
        p.text = "Coursera Use-Case Presentation · Deep Learning Specialization · PEC2 / OE1"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_LIGHT

        # Slide Number
        tx_num = slide.shapes.add_textbox(Inches(10.5), Inches(7.05), Inches(2.033), Inches(0.35))
        tf_num = tx_num.text_frame
        tf_num.margin_top = tf_num.margin_bottom = tf_num.margin_left = tf_num.margin_right = 0
        p_num = tf_num.paragraphs[0]
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.text = f"{slide_num:02d}"
        p_num.font.name = FONT_FAMILY
        p_num.font.size = Pt(9.5)
        p_num.font.bold = True
        p_num.font.color.rgb = ACCENT_EMERALD

    def add_slide_header(slide, section_tag, title_text, subtitle_text=None):
        # Section Category Pill / Tag
        tx_tag = slide.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(11.733), Inches(0.3))
        tf_tag = tx_tag.text_frame
        tf_tag.margin_top = tf_tag.margin_bottom = tf_tag.margin_left = tf_tag.margin_right = 0
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = section_tag.upper()
        p_tag.font.name = FONT_FAMILY
        p_tag.font.size = Pt(10.5)
        p_tag.font.bold = True
        p_tag.font.color.rgb = ACCENT_EMERALD

        # Title
        tx_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.733), Inches(0.5))
        tf_title = tx_title.text_frame
        tf_title.margin_top = tf_title.margin_bottom = tf_title.margin_left = tf_title.margin_right = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = FONT_FAMILY
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_MAIN

        # Optional Subtitle
        if subtitle_text:
            tx_sub = slide.shapes.add_textbox(Inches(0.8), Inches(1.38), Inches(11.733), Inches(0.35))
            tf_sub = tx_sub.text_frame
            tf_sub.margin_top = tf_sub.margin_bottom = tf_sub.margin_left = tf_sub.margin_right = 0
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = subtitle_text
            p_sub.font.name = FONT_FAMILY
            p_sub.font.size = Pt(12)
            p_sub.font.color.rgb = TEXT_MUTED

    def create_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    apply_background(slide1)

    # Accent decorative top bar
    bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(1.5), Inches(0.06))
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT_EMERALD
    bar.line.color.rgb = ACCENT_EMERALD

    # Top Tag
    tx1_tag = slide1.shapes.add_textbox(Inches(0.8), Inches(1.05), Inches(11.5), Inches(0.4))
    tf1_tag = tx1_tag.text_frame
    p = tf1_tag.paragraphs[0]
    p.text = "COURSERA USE-CASE PRESENTATION · PEC2 / OE1"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_EMERALD

    # Main Title
    tx1_title = slide1.shapes.add_textbox(Inches(0.8), Inches(1.55), Inches(11.7), Inches(1.2))
    tf1_title = tx1_title.text_frame
    p = tf1_title.paragraphs[0]
    p.text = "Deep Learning Specialization"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN

    # Subtitle
    tx1_sub = slide1.shapes.add_textbox(Inches(0.8), Inches(2.75), Inches(11.7), Inches(0.8))
    tf1_sub = tx1_sub.text_frame
    p = tf1_sub.paragraphs[0]
    p.text = "A practical, real-world use case built on the concepts learned in this certification:\nAutomated 15-Class Vegetable Species Classification System using ResNet-18"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(16)
    p.font.color.rgb = TEXT_MUTED

    # Presenter Information Card
    create_card(slide1, Inches(0.8), Inches(4.0), Inches(11.733), Inches(2.3), bg_color=CARD_BG, border_color=CARD_BORDER)

    # Card Content
    tx_meta = slide1.shapes.add_textbox(Inches(1.2), Inches(4.3), Inches(10.9), Inches(1.7))
    tf_meta = tx_meta.text_frame
    
    p = tf_meta.paragraphs[0]
    p.text = "Presented by:"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_LIGHT

    p = tf_meta.add_paragraph()
    p.text = "Krushna Prakash Thakare"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN
    p.space_after = Pt(6)

    p = tf_meta.add_paragraph()
    p.text = "TY AIDS  ·  Div G  ·  PRN: 12520029  ·  Roll No. 32"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_EMERALD
    p.space_after = Pt(4)

    p = tf_meta.add_paragraph()
    p.text = "Department of Artificial Intelligence & Data Science · Vishwakarma Institute of Technology, Pune"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    add_footer(slide1, 1)

    # =========================================================================
    # SLIDE 2: AGENDA
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    apply_background(slide2)
    add_slide_header(slide2, "Agenda", "What We'll Cover", "A systematic overview of certification competencies and real-world deployment")

    agenda_items = [
        ("01", "Certification Overview", "DeepLearning.AI specialization details, instructor, course breakdown, and verification"),
        ("02", "Key Concepts & Technologies", "Deep learning paradigms: CNNs, ResNet skip connections, transfer learning, regularization"),
        ("03", "Use-Case Problem Statement", "Agricultural & retail challenges in manual vegetable identification and visual classification"),
        ("04", "Proposed Solution & Architecture", "End-to-end deep learning framework leveraging fine-tuned ResNet-18 and Flask backend"),
        ("05", "Implementation Approach", "Data augmentation pipeline, model evaluation metrics, and live responsive web dashboard"),
        ("06", "Conclusion & Key Takeaways", "Core competencies acquired, business/societal value, and scalable future extensions")
    ]

    for idx, (num, title, desc) in enumerate(agenda_items):
        col = idx % 2
        row = idx // 2
        left = Inches(0.8 + col * 5.96)
        top = Inches(1.95 + row * 1.55)
        
        # Card shape
        create_card(slide2, left, top, Inches(5.76), Inches(1.38))

        # Text box
        tx_box = slide2.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), Inches(5.26), Inches(1.0))
        tf = tx_box.text_frame
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        
        p = tf.paragraphs[0]
        p.text = f"{num}  ·  {title}"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_FAMILY
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_before = Pt(4)

    add_footer(slide2, 2)

    # =========================================================================
    # SLIDE 3: 01 · CERTIFICATION OVERVIEW
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    apply_background(slide3)
    add_slide_header(slide3, "01 · Certification Overview", "Deep Learning Specialization", "Comprehensive 5-course specialization authorized by DeepLearning.AI and offered via Coursera")

    # 4 Overview Cards across the top
    top_cards = [
        ("01", "Provider", "DeepLearning.AI", "Offered through Coursera\nTaught by Andrew Ng"),
        ("02", "Duration", "5 Courses", "4 Months intensive training\nHands-on PyTorch & TF labs"),
        ("03", "Domain", "Artificial Intelligence", "Deep Learning, CNNs,\nComputer Vision & Optimization"),
        ("04", "Completed On", "October 20, 2026", "Specialization Verified\nID: NT54B87LDO1B")
    ]

    card_width = Inches(2.78)
    for i, (num, label, primary, sub) in enumerate(top_cards):
        left = Inches(0.8 + i * 2.98)
        top = Inches(1.9)
        create_card(slide3, left, top, card_width, Inches(1.75))

        tx = slide3.shapes.add_textbox(left + Inches(0.2), top + Inches(0.18), card_width - Inches(0.4), Inches(1.4))
        tf = tx.text_frame
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

        p = tf.paragraphs[0]
        p.text = f"{num} · {label.upper()}"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = ACCENT_EMERALD

        p = tf.add_paragraph()
        p.text = primary
        p.font.name = FONT_FAMILY
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(3)

        p = tf.add_paragraph()
        p.text = sub
        p.font.name = FONT_FAMILY
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(3)

    # Bottom Specialization Course Breakdown Card
    create_card(slide3, Inches(0.8), Inches(3.85), Inches(11.733), Inches(2.95))

    tx_courses = slide3.shapes.add_textbox(Inches(1.1), Inches(4.05), Inches(11.133), Inches(2.6))
    tf_c = tx_courses.text_frame
    tf_c.margin_top = tf_c.margin_bottom = tf_c.margin_left = tf_c.margin_right = 0

    p = tf_c.paragraphs[0]
    p.text = "Courses Completed within Specialization & Credential Verifications"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN
    p.space_after = Pt(8)

    course_list = [
        ("Course 1: Neural Networks and Deep Learning", "Completed: Aug 27, 2026", "Verify ID: IXG7ID9BPCYF"),
        ("Course 2: Improving Deep Neural Networks: Hyperparameter Tuning, Regularization & Optimization", "Completed: Aug 27, 2026", "Verify ID: 1AL1GBGIMUGV"),
        ("Course 3: Structuring Machine Learning Projects", "Completed: Aug 27, 2026", "Verify ID: YFH2P1JLT4VQ"),
        ("Course 4: Convolutional Neural Networks (CNNs)", "Completed: Oct 8, 2026", "Verify ID: UMJ0IFGKPJGP"),
        ("Course 5: Sequence Models", "Completed: Oct 20, 2026", "Verify ID: IS6DCURTSPUY")
    ]

    for c_title, c_date, c_id in course_list:
        p = tf_c.add_paragraph()
        p.text = f"•  {c_title}  —  {c_date}  |  {c_id}"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(4)

    add_footer(slide3, 3)

    # =========================================================================
    # SLIDE 4: 02 · KEY CONCEPTS & TECHNOLOGIES
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    apply_background(slide4)
    add_slide_header(slide4, "02 · Key Concepts & Technologies", "What This Certification Covers", "Theoretical foundations and modern tooling applied directly to computer vision workflows")

    # Table layout
    rows, cols = 5, 3
    left, top, width, height = Inches(0.8), Inches(1.9), Inches(11.733), Inches(4.8)
    table_shape = slide4.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    table.columns[0].width = Inches(3.2)
    table.columns[1].width = Inches(5.733)
    table.columns[2].width = Inches(2.8)

    headers = ["Topic / Module", "Core Concepts Learned", "Tools & Technologies"]
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = ACCENT_LIGHT
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = FONT_FAMILY
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = ACCENT_EMERALD

    table_data = [
        ("Convolutional Neural Networks (CNNs)",
         "Deep residual connections (ResNet-18 skip layers), convolutional kernels, spatial feature hierarchies, max pooling, and receptive field expansion.",
         "PyTorch, Torchvision, ResNet-18 Backbone"),
        ("Transfer Learning & Fine-Tuning",
         "Pretrained ImageNet weight transfer, convolutional layer freezing, fully connected classification head replacement for custom 15-class prediction.",
         "torchvision.models, Linear Classification Head"),
        ("Hyperparameter Tuning & Regularization",
         "Data augmentation (Resize 224x224, Random transforms), Cross-Entropy loss calculation, Adam/SGD optimization, batch processing, and Softmax distribution.",
         "torch.optim, transforms.Compose, DataLoader"),
        ("ML Structuring & Production Deployment",
         "Train/Validation/Test dataset partitioning, confusion matrix diagnostics, precision/recall metrics, RESTful API architecture, and interactive web dashboard.",
         "Flask, Scikit-learn, Seaborn, HTML5 / Tailwind CSS")
    ]

    for i, row in enumerate(table_data, start=1):
        for j, text in enumerate(row):
            cell = table.cell(i, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.name = FONT_FAMILY
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_MAIN if j == 0 else TEXT_MUTED
            if j == 0:
                p.font.bold = True

    add_footer(slide4, 4)

    # =========================================================================
    # SLIDE 5: 03 · USE-CASE PROBLEM STATEMENT
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    apply_background(slide5)
    add_slide_header(slide5, "03 · Use-Case Problem Statement", 
                     "Automated 15-Class Vegetable Species Classification for Agritech & Retail", 
                     "Overcoming bottlenecks in automated produce sorting, inventory control, and cashierless retail")

    # Core Problem Statement Banner
    create_card(slide5, Inches(0.8), Inches(1.85), Inches(11.733), Inches(0.85), bg_color=ACCENT_LIGHT, border_color=ACCENT_BORDER)
    tx_banner = slide5.shapes.add_textbox(Inches(1.1), Inches(1.95), Inches(11.133), Inches(0.65))
    tf_b = tx_banner.text_frame
    tf_b.margin_top = tf_b.margin_bottom = tf_b.margin_left = tf_b.margin_right = 0
    p = tf_b.paragraphs[0]
    p.text = "CORE PROBLEM STATEMENT:"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = ACCENT_EMERALD
    p = tf_b.add_paragraph()
    p.text = "Manual vegetable identification in modern agricultural supply chains and retail checkouts is slow, error-prone, and unsustainable at scale due to high morphological variability and inter-class visual similarity."
    p.font.name = FONT_FAMILY
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN

    # 3 Structured Columns: Who is affected, Why it matters, Current gap
    pillars = [
        ("Who is Affected", 
         "Target Stakeholders",
         "• Agricultural post-harvest sorting and grading warehouses.\n• Smart retail & supermarkets (automated barcode-free checkout).\n• Wholesale produce supply chains and cold storage distribution.\n• Consumers using nutritional intake and dietary logging applications."),
        
        ("Why it Matters", 
         "Economic & Operational Impact",
         "• High Labor Costs: Manual grading requires continuous human staffing.\n• Sorting Delays: Visual bottlenecks reduce perishable shelf-life.\n• Mispricing & Shrinkage: Cashier misidentifications cause substantial inventory loss.\n• Customer Experience: Checkout queues lengthened by barcode lookups."),
        
        ("Current Gap", 
         "Limitations of Existing Methods",
         "• Traditional Computer Vision: Color/edge heuristics fail under variable lighting and irregular angles.\n• High Inter-Class Similarity: Variants like Bitter Gourd vs. Cucumber or Bottle Gourd vs. Papaya mislead basic filters.\n• Non-Rigid Morphology: Organic vegetables exhibit continuous shape, texture, and size variations.")
    ]

    card_w = Inches(3.75)
    for i, (tag, title, body) in enumerate(pillars):
        left = Inches(0.8 + i * 3.99)
        top = Inches(2.95)
        create_card(slide5, left, top, card_w, Inches(3.85))

        tx = slide5.shapes.add_textbox(left + Inches(0.25), top + Inches(0.25), card_w - Inches(0.5), Inches(3.35))
        tf = tx.text_frame
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

        p = tf.paragraphs[0]
        p.text = tag.upper()
        p.font.name = FONT_FAMILY
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = ACCENT_EMERALD

        p = tf.add_paragraph()
        p.text = title
        p.font.name = FONT_FAMILY
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(8)

        p = tf.add_paragraph()
        p.text = body
        p.font.name = FONT_FAMILY
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MUTED

    add_footer(slide5, 5)

    # =========================================================================
    # SLIDE 6: 04 · PROPOSED SOLUTION
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    apply_background(slide6)
    add_slide_header(slide6, "04 · Proposed Solution", "How the Certification's Concepts Solve It", "A transfer-learning-based deep vision pipeline engineered for low latency and high accuracy")

    # Left Column: Approach & Expected Outcomes
    left_w = Inches(5.7)
    create_card(slide6, Inches(0.8), Inches(1.9), left_w, Inches(4.85))

    tx_sol = slide6.shapes.add_textbox(Inches(1.1), Inches(2.15), left_w - Inches(0.6), Inches(4.35))
    tf_s = tx_sol.text_frame
    tf_s.margin_top = tf_s.margin_bottom = tf_s.margin_left = tf_s.margin_right = 0

    p = tf_s.paragraphs[0]
    p.text = "SOLUTION APPROACH"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_EMERALD

    p = tf_s.add_paragraph()
    p.text = "End-to-End Deep Learning Architecture"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN
    p.space_after = Pt(6)

    p = tf_s.add_paragraph()
    p.text = "We built a production-ready vision system that utilizes a transfer-learned ResNet-18 convolutional backbone to accurately classify vegetable images across 15 botanical classes. The model is integrated with a lightweight Flask REST API and a modern web dashboard for instant single-image classification, certainty scoring, and botanical insights."
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED
    p.space_after = Pt(14)

    p = tf_s.add_paragraph()
    p.text = "EXPECTED OUTCOMES & METRICS"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_EMERALD

    outcomes = [
        "• Classification Accuracy: >98% overall test accuracy across all 15 classes.",
        "• Ultra-Low Latency: Average inference time under 40ms per image.",
        "• Throughput Acceleration: Eliminates manual visual check delays by 95%.",
        "• High Reliability: Softmax confidence scoring prevents false positive misclassifications."
    ]
    for o in outcomes:
        p = tf_s.add_paragraph()
        p.text = o
        p.font.name = FONT_FAMILY
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(3)

    # Right Column: Certification Concepts Applied
    right_w = Inches(5.733)
    create_card(slide6, Inches(6.8), Inches(1.9), right_w, Inches(4.85))

    tx_cnc = slide6.shapes.add_textbox(Inches(7.1), Inches(2.15), right_w - Inches(0.6), Inches(4.35))
    tf_c = tx_cnc.text_frame
    tf_c.margin_top = tf_c.margin_bottom = tf_c.margin_left = tf_c.margin_right = 0

    p = tf_c.paragraphs[0]
    p.text = "CERTIFICATION CONCEPTS APPLIED"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_EMERALD

    p = tf_c.add_paragraph()
    p.text = "Theoretical Principles from Deep Learning Specialization"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN
    p.space_after = Pt(8)

    concepts = [
        ("Residual Learning (ResNet-18)", 
         "Utilizes identity shortcut connections (skip connections) allowing gradients to propagate directly, preventing vanishing gradients in deeper feature extractors."),
        ("Transfer Learning via Pretrained Weights", 
         "Leveraged ImageNet features pretrained on 1.2M images, freezing low-level visual filters and retraining the final fully connected layer for rapid convergence."),
        ("Multi-Class Cross-Entropy & Softmax Loss", 
         "Trained with categorical cross-entropy loss, producing well-calibrated class probability vectors for fine-grained ranking across 15 species."),
        ("Input Normalization & Tensor Pipelines", 
         "Employed standardized 224x224 tensor reshaping, scaling to [0,1], and RGB color channel formatting for optimal receptive field compatibility.")
    ]

    for title, desc in concepts:
        p = tf_c.add_paragraph()
        p.text = f"• {title}:"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN

        p = tf_c.add_paragraph()
        p.text = desc
        p.font.name = FONT_FAMILY
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(4)

    add_footer(slide6, 6)

    # =========================================================================
    # SLIDE 7: 05 · IMPLEMENTATION APPROACH
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    apply_background(slide7)
    add_slide_header(slide7, "05 · Implementation Approach", "From Concept to Working Solution", "Three-stage deployment pipeline spanning user interaction, deep learning inference, and UI rendering")

    # 3 Horizontal Process Blocks (Input -> Processing -> Output)
    flow_steps = [
        ("STAGE 1", "Image Input & Ingestion", 
         "• User selects photo via drag-and-drop, direct clipboard paste (Ctrl+V), or file browser.\n• Image decoded into RGB mode using Pillow.\n• Resized to 224x224 and converted to PyTorch FloatTensor."),
        
        ("STAGE 2", "Deep ResNet-18 Inference", 
         "• Tensor forwarded through 18-layer ResNet.\n• Convolutional layers extract hierarchical spatial edges, textures, and shape features.\n• Custom 15-output linear layer generates logits; Softmax computes probabilities."),
        
        ("STAGE 3", "Interactive Dashboard Output", 
         "• Prediction JSON delivered to client via Flask REST API.\n• UI highlights primary species, emoji, and certainty tag.\n• Displays Top-5 probability distribution meters and botanical/nutritional profile.")
    ]

    card_flow_w = Inches(3.75)
    for i, (stage, title, body) in enumerate(flow_steps):
        left = Inches(0.8 + i * 3.99)
        top = Inches(1.85)
        create_card(slide7, left, top, card_flow_w, Inches(2.25))

        tx = slide7.shapes.add_textbox(left + Inches(0.2), top + Inches(0.18), card_flow_w - Inches(0.4), Inches(1.9))
        tf = tx.text_frame
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

        p = tf.paragraphs[0]
        p.text = stage
        p.font.name = FONT_FAMILY
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = ACCENT_EMERALD

        p = tf.add_paragraph()
        p.text = title
        p.font.name = FONT_FAMILY
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(4)

        p = tf.add_paragraph()
        p.text = body
        p.font.name = FONT_FAMILY
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_MUTED

    # Bottom Area: Actual Project Results & Architecture Specs
    create_card(slide7, Inches(0.8), Inches(4.3), Inches(11.733), Inches(2.5))

    # Check if plot images exist in logs
    plot_path = r"logs\Resnet18_results\plot_Resnet18.png"
    cm_path = r"logs\Resnet18_results\confusion_matrix.png"

    has_plots = os.path.exists(plot_path) and os.path.exists(cm_path)
    if has_plots:
        # Embed actual training plot
        slide7.shapes.add_picture(plot_path, Inches(1.1), Inches(4.45), Inches(3.4), Inches(2.2))
        # Embed confusion matrix
        slide7.shapes.add_picture(cm_path, Inches(4.7), Inches(4.45), Inches(2.2), Inches(2.2))
        
        # Right text box describing the empirical validation
        tx_res = slide7.shapes.add_textbox(Inches(7.1), Inches(4.45), Inches(5.1), Inches(2.2))
        tf_r = tx_res.text_frame
        tf_r.margin_top = tf_r.margin_bottom = tf_r.margin_left = tf_r.margin_right = 0

        p = tf_r.paragraphs[0]
        p.text = "EMPIRICAL MODEL VALIDATION & PERFORMANCE"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = ACCENT_EMERALD

        specs = [
            ("Dataset", "15 Classes: Bean, Bitter Gourd, Bottle Gourd, Brinjal, Broccoli, Cabbage, Capsicum, Carrot, Cauliflower, Cucumber, Papaya, Potato, Pumpkin, Radish, Tomato"),
            ("Training & Loss", "Rapid convergence within 10 epochs using transfer learning; validation loss consistently tracking training loss without overfitting."),
            ("Confusion Matrix", "High diagonal density across all 15 classes demonstrating strong inter-class discriminability."),
            ("System Stack", "PyTorch 2.x · Torchvision · Flask REST API · Tailwind CSS · Vanilla JavaScript")
        ]
        for k, v in specs:
            p = tf_r.add_paragraph()
            p.text = f"• {k}: {v}"
            p.font.name = FONT_FAMILY
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_MUTED
            p.space_before = Pt(2)
    else:
        # Fallback text box if plots not found
        tx_res = slide7.shapes.add_textbox(Inches(1.1), Inches(4.45), Inches(11.1), Inches(2.2))
        tf_r = tx_res.text_frame
        p = tf_r.paragraphs[0]
        p.text = "SYSTEM ARCHITECTURE & EMPIRICAL VALIDATION"
        p.font.bold = True
        p.font.color.rgb = ACCENT_EMERALD

    add_footer(slide7, 7)

    # =========================================================================
    # SLIDE 8: 06 · CONCLUSION & TAKEAWAYS
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    apply_background(slide8)
    add_slide_header(slide8, "06 · Conclusion", "Key Takeaways & Future Directions", "Synthesizing deep learning theory with tangible industry value and scalability")

    concl_cards = [
        ("SKILLS GAINED", "Certification Competencies",
         "• Architecting deep convolutional neural networks (CNNs) from scratch and pretrained weights.\n• Implementing residual learning (ResNet) to train deep models without vanishing gradients.\n• Fine-tuning hyperparameters, regularization, and optimization schemes (Adam, Cross-Entropy).\n• Productionizing PyTorch models into low-latency REST APIs and responsive web interfaces."),
        
        ("REAL-WORLD VALUE", "Tangible Industry Impact",
         "• High Precision Sorting: Enables automated sorting lines to classify 15 vegetable varieties at scale.\n• Reduced Checkout Latency: Seamlessly integrates into smart retail checkouts without barcode scanning.\n• Economic Efficiency: Minimizes human inspection labor and prevents mispricing losses.\n• User Education: Delivers instant nutritional and botanical facts alongside classification."),
        
        ("NEXT STEPS", "Scalable Extensions",
         "• Freshness & Defect Detection: Multi-task learning for simultaneous species and rot detection.\n• Edge Optimization: Export model to ONNX, TensorRT, or TorchScript for real-time edge microcontrollers.\n• Expanded Taxonomy: Scale dataset to 50+ regional exotic vegetables and leafy greens.\n• Mobile App Integration: Deploy camera-based scanning via Flutter/React Native for field farmers.")
    ]

    card_w8 = Inches(3.75)
    for i, (tag, title, body) in enumerate(concl_cards):
        left = Inches(0.8 + i * 3.99)
        top = Inches(1.9)
        create_card(slide8, left, top, card_w8, Inches(3.6))

        tx = slide8.shapes.add_textbox(left + Inches(0.25), top + Inches(0.25), card_w8 - Inches(0.5), Inches(3.1))
        tf = tx.text_frame
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

        p = tf.paragraphs[0]
        p.text = tag
        p.font.name = FONT_FAMILY
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = ACCENT_EMERALD

        p = tf.add_paragraph()
        p.text = title
        p.font.name = FONT_FAMILY
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(6)

        p = tf.add_paragraph()
        p.text = body
        p.font.name = FONT_FAMILY
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_MUTED

    # Bottom Thank You Banner
    create_card(slide8, Inches(0.8), Inches(5.7), Inches(11.733), Inches(1.05), bg_color=ACCENT_LIGHT, border_color=ACCENT_BORDER)
    tx_ty = slide8.shapes.add_textbox(Inches(1.0), Inches(5.8), Inches(11.333), Inches(0.85))
    tf_ty = tx_ty.text_frame
    tf_ty.margin_top = tf_ty.margin_bottom = tf_ty.margin_left = tf_ty.margin_right = 0
    p = tf_ty.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "Thank You  ·  Questions & Answers"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_EMERALD

    p2 = tf_ty.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    p2.text = "Krushna Prakash Thakare  ·  TY AIDS (Div G)  ·  Vishwakarma Institute of Technology, Pune"
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(11)
    p2.font.color.rgb = TEXT_MUTED

    add_footer(slide8, 8)

    # Save presentation
    output_filename = "Coursera_Deep_Learning_Use_Case_Presentation.pptx"
    prs.save(output_filename)
    print(f"Presentation saved successfully to: {output_filename}")

if __name__ == "__main__":
    create_deck()

