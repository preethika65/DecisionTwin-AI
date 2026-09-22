from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def safe_text(value):

    if value is None:
        return ""

    if isinstance(value, list):

        return ", ".join(
            str(item)
            for item in value
        )

    if isinstance(value, dict):

        return ", ".join(
            f"{key}: {value}"
            for key, value in value.items()
        )

    return str(value)


def get_response_text(item):

    if not isinstance(item, dict):
        return safe_text(item)

    if "response" in item:
        return safe_text(item["response"])

    if "answer" in item:
        return safe_text(item["answer"])

    return ""


def get_persona_name(item):

    if not isinstance(item, dict):
        return "Synthetic User"

    if "persona" in item:

        persona = item["persona"]

        if isinstance(persona, dict):
            return safe_text(
                persona.get(
                    "name",
                    "Synthetic User"
                )
            )

        return safe_text(persona)

    if "persona_name" in item:
        return safe_text(
            item["persona_name"]
        )

    return safe_text(
        item.get(
            "name",
            "Synthetic User"
        )
    )


# =========================================================
# PDF HEADER / FOOTER
# =========================================================

def add_page_number(canvas, doc):

    canvas.saveState()

    canvas.setFont(
        "Helvetica",
        8
    )

    canvas.drawCentredString(
        A4[0] / 2,
        10 * mm,
        f"DecisionTwin AI | Page {doc.page}"
    )

    canvas.restoreState()


# =========================================================
# CREATE RESEARCH REPORT
# =========================================================

def create_research_report(
    filename,
    personas,
    question,
    responses,
    insights,
    rating,
    themes,
    sentiment,
    quotes
):

    # -----------------------------------------------------
    # DOCUMENT
    # -----------------------------------------------------

    document = SimpleDocTemplate(

        filename,

        pagesize=A4,

        rightMargin=18 * mm,
        leftMargin=18 * mm,

        topMargin=18 * mm,
        bottomMargin=18 * mm

    )

    # -----------------------------------------------------
    # STYLES
    # -----------------------------------------------------

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(

        "ReportTitle",

        parent=styles["Title"],

        fontSize=24,

        leading=28,

        alignment=TA_CENTER,

        spaceAfter=10

    )

    subtitle_style = ParagraphStyle(

        "Subtitle",

        parent=styles["Normal"],

        fontSize=11,

        leading=16,

        alignment=TA_CENTER,

        spaceAfter=20

    )

    heading_style = ParagraphStyle(

        "Heading",

        parent=styles["Heading2"],

        fontSize=16,

        leading=20,

        spaceBefore=12,

        spaceAfter=8

    )

    subheading_style = ParagraphStyle(

        "SubHeading",

        parent=styles["Heading3"],

        fontSize=12,

        leading=16,

        spaceBefore=8,

        spaceAfter=5

    )

    body_style = ParagraphStyle(

        "Body",

        parent=styles["BodyText"],

        fontSize=9.5,

        leading=14,

        spaceAfter=6

    )

    small_style = ParagraphStyle(

        "Small",

        parent=styles["BodyText"],

        fontSize=8.5,

        leading=12

    )

    quote_style = ParagraphStyle(

        "Quote",

        parent=styles["BodyText"],

        fontSize=9.5,

        leading=14,

        leftIndent=10,

        rightIndent=10,

        spaceAfter=5

    )

    # -----------------------------------------------------
    # STORY
    # -----------------------------------------------------

    story = []

    # =====================================================
    # COVER
    # =====================================================

    story.append(
        Spacer(
            1,
            35 * mm
        )
    )

    story.append(
        Paragraph(
            "DecisionTwin AI",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Synthetic User Research Report",
            subtitle_style
        )
    )

    story.append(
        Paragraph(
            "Insights & Experiment Results",
            heading_style
        )
    )

    story.append(
        Paragraph(
            "AI-powered analysis of synthetic customer "
            "personas, survey responses, themes, sentiment "
            "and product validation.",
            body_style
        )
    )

    story.append(
        Spacer(
            1,
            15 * mm
        )
    )

    story.append(
        Paragraph(
            f"<b>Research Question:</b> "
            f"{safe_text(question)}",
            body_style
        )
    )

    story.append(
        Paragraph(
            f"<b>Total Synthetic Users:</b> "
            f"{len(personas)}",
            body_style
        )
    )

    story.append(
        Spacer(
            1,
            20 * mm
        )
    )

    story.append(
        Paragraph(
            "Generated by DecisionTwin AI",
            subtitle_style
        )
    )

    story.append(
        PageBreak()
    )

    # =====================================================
    # 1. EXPERIMENT OVERVIEW
    # =====================================================

    story.append(
        Paragraph(
            "1. Experiment Overview",
            heading_style
        )
    )

    positive = 0
    neutral = 0
    negative = 0

    if isinstance(sentiment, dict):

        positive = sentiment.get(
            "positive",
            0
        )

        neutral = sentiment.get(
            "neutral",
            0
        )

        negative = sentiment.get(
            "negative",
            0
        )

    response_count = len(responses)

    if response_count > 0:

        positive_rate = round(
            positive /
            response_count *
            100,
            1
        )

    else:

        positive_rate = 0

    overview_data = [

        [
            "Metric",
            "Value"
        ],

        [
            "Synthetic Users",
            str(len(personas))
        ],

        [
            "Survey Responses",
            str(response_count)
        ],

        [
            "Positive Responses",
            str(positive)
        ],

        [
            "Neutral Responses",
            str(neutral)
        ],

        [
            "Negative Responses",
            str(negative)
        ],

        [
            "Positive Response Rate",
            f"{positive_rate}%"
        ]

    ]

    overview_table = Table(

        overview_data,

        colWidths=[
            80 * mm,
            70 * mm
        ]

    )

    overview_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor(
                    "#1e293b"
                )
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "FONTNAME",
                (0, 1),
                (-1, -1),
                "Helvetica"
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            )

        ])
    )

    story.append(
        overview_table
    )

    story.append(
        Spacer(
            1,
            10 * mm
        )
    )

    # =====================================================
    # 2. PRODUCT VALIDATION
    # =====================================================

    story.append(
        Paragraph(
            "2. Product Validation",
            heading_style
        )
    )

    score = rating.get(
        "score",
        0
    )

    recommendation = rating.get(
        "recommendation",
        "Not available"
    )

    reason = rating.get(
        "reason",
        ""
    )

    validation_data = [

        [
            "Product Validation Score",
            f"{score}/100"
        ],

        [
            "Recommendation",
            safe_text(
                recommendation
            )
        ],

        [
            "Reason",
            safe_text(reason)
        ]

    ]

    validation_table = Table(

        validation_data,

        colWidths=[
            65 * mm,
            85 * mm
        ]

    )

    validation_table.setStyle(
        TableStyle([

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor(
                    "#e2e8f0"
                )
            ),

            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                8
            )

        ])
    )

    story.append(
        validation_table
    )

    # =====================================================
    # 3. PERSONA PROFILES
    # =====================================================

    story.append(
        Paragraph(
            "3. Synthetic Persona Profiles",
            heading_style
        )
    )

    if personas:

        for index, persona in enumerate(
            personas,
            start=1
        ):

            name = persona.get(
                "name",
                f"Persona {index}"
            )

            age = persona.get(
                "age",
                ""
            )

            gender = persona.get(
                "gender",
                ""
            )

            location = persona.get(
                "location",
                ""
            )

            occupation = persona.get(
                "occupation",
                ""
            )

            personality = persona.get(
                "personality",
                ""
            )

            interests = persona.get(
                "interests",
                persona.get(
                    "interest",
                    ""
                )
            )

            buying_behavior = persona.get(
                "buying_behavior",
                ""
            )

            pain_points = persona.get(
                "pain_points",
                ""
            )

            persona_data = [

                [
                    "Field",
                    "Profile"
                ],

                [
                    "Name",
                    safe_text(name)
                ],

                [
                    "Age",
                    safe_text(age)
                ],

                [
                    "Gender",
                    safe_text(gender)
                ],

                [
                    "Location",
                    safe_text(location)
                ],

                [
                    "Occupation",
                    safe_text(occupation)
                ],

                [
                    "Personality",
                    safe_text(personality)
                ],

                [
                    "Interests",
                    safe_text(interests)
                ],

                [
                    "Buying Behavior",
                    safe_text(
                        buying_behavior
                    )
                ],

                [
                    "Pain Points",
                    safe_text(
                        pain_points
                    )
                ]

            ]

            persona_table = Table(

                persona_data,

                colWidths=[
                    42 * mm,
                    108 * mm
                ]

            )

            persona_table.setStyle(
                TableStyle([

                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        colors.grey
                    ),

                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor(
                            "#334155"
                        )
                    ),

                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white
                    ),

                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold"
                    ),

                    (
                        "BACKGROUND",
                        (0, 1),
                        (0, -1),
                        colors.HexColor(
                            "#f1f5f9"
                        )
                    ),

                    (
                        "FONTNAME",
                        (0, 1),
                        (0, -1),
                        "Helvetica-Bold"
                    ),

                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    ),

                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        8
                    ),

                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    ),

                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    )

                ])
            )

            story.append(
                Paragraph(
                    f"Persona {index}",
                    subheading_style
                )
            )

            story.append(
                persona_table
            )

            story.append(
                Spacer(
                    1,
                    7 * mm
                )
            )

    else:

        story.append(
            Paragraph(
                "No persona profiles available.",
                body_style
            )
        )

    story.append(
        PageBreak()
    )

    # =====================================================
    # 4. SURVEY RESPONSES
    # =====================================================

    story.append(
        Paragraph(
            "4. Survey Responses",
            heading_style
        )
    )

    story.append(
        Paragraph(
            f"<b>Question:</b> "
            f"{safe_text(question)}",
            body_style
        )
    )

    if responses:

        response_data = [

            [
                "Persona",
                "Response"
            ]

        ]

        for item in responses:

            response_data.append([

                get_persona_name(item),

                get_response_text(item)

            ])

        response_table = Table(

            response_data,

            colWidths=[
                48 * mm,
                102 * mm
            ],

            repeatRows=1

        )

        response_table.setStyle(
            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(
                        "#1e293b"
                    )
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.grey
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),

                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    8
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )

            ])
        )

        story.append(
            response_table
        )

    else:

        story.append(
            Paragraph(
                "No survey responses available.",
                body_style
            )
        )

    # =====================================================
    # 5. THEME CLUSTERS
    # =====================================================

    story.append(
        Paragraph(
            "5. Theme Clusters",
            heading_style
        )
    )

    if themes:

        theme_data = [

            [
                "Theme",
                "Count",
                "Percentage",
                "Summary"
            ]

        ]

        for theme, data in themes.items():

            if isinstance(data, dict):

                theme_data.append([

                    safe_text(theme),

                    safe_text(
                        data.get(
                            "count",
                            0
                        )
                    ),

                    safe_text(
                        data.get(
                            "percentage",
                            0
                        )
                    ),

                    safe_text(
                        data.get(
                            "summary",
                            ""
                        )
                    )

                ])

        if len(theme_data) > 1:

            theme_table = Table(

                theme_data,

                colWidths=[
                    35 * mm,
                    20 * mm,
                    25 * mm,
                    70 * mm
                ],

                repeatRows=1

            )

            theme_table.setStyle(
                TableStyle([

                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor(
                            "#1e293b"
                        )
                    ),

                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white
                    ),

                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold"
                    ),

                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        colors.grey
                    ),

                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    ),

                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        7.5
                    ),

                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    ),

                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    )

                ])
            )

            story.append(
                theme_table
            )

    else:

        story.append(
            Paragraph(
                "No theme analysis available.",
                body_style
            )
        )

    # =====================================================
    # 6. SENTIMENT
    # =====================================================

    story.append(
        Paragraph(
            "6. Sentiment Breakdown",
            heading_style
        )
    )

    sentiment_data = [

        [
            "Sentiment",
            "Responses"
        ],

        [
            "Positive",
            str(positive)
        ],

        [
            "Neutral",
            str(neutral)
        ],

        [
            "Negative",
            str(negative)
        ]

    ]

    sentiment_table = Table(

        sentiment_data,

        colWidths=[
            75 * mm,
            75 * mm
        ]

    )

    sentiment_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor(
                    "#1e293b"
                )
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.4,
                colors.grey
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            )

        ])
    )

    story.append(
        sentiment_table
    )

    # =====================================================
    # 7. KEY PERSONA QUOTES
    # =====================================================

    story.append(
        Paragraph(
            "7. Key Persona Quotes",
            heading_style
        )
    )

    if quotes:

        for index, item in enumerate(
            quotes,
            start=1
        ):

            if isinstance(item, dict):

                quote = safe_text(
                    item.get(
                        "quote",
                        ""
                    )
                )

                persona = safe_text(
                    item.get(
                        "persona",
                        "Synthetic User"
                    )
                )

            else:

                quote = safe_text(item)
                persona = "Synthetic User"

            story.append(
                Paragraph(
                    f'“{quote}”',
                    quote_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>— {persona}</b>",
                    small_style
                )
            )

            story.append(
                Spacer(
                    1,
                    3 * mm
                )
            )

    else:

        story.append(
            Paragraph(
                "No key quotes available.",
                body_style
            )
        )

    # =====================================================
    # 8. AI RESEARCH INSIGHTS
    # =====================================================

    story.append(
        Paragraph(
            "8. AI Research Insights",
            heading_style
        )
    )

    if insights:

        insight_lines = str(
            insights
        ).split("\n")

        for line in insight_lines:

            line = line.strip()

            if line:

                story.append(
                    Paragraph(
                        line,
                        body_style
                    )
                )

    else:

        story.append(
            Paragraph(
                "No AI research insights generated.",
                body_style
            )
        )

    # =====================================================
    # 9. FINAL SUMMARY
    # =====================================================

    story.append(
        PageBreak()
    )

    story.append(
        Paragraph(
            "9. Final Research Summary",
            heading_style
        )
    )

    story.append(
        Paragraph(

            f"DecisionTwin AI analyzed "
            f"{len(personas)} synthetic users "
            f"and {len(responses)} survey responses.",

            body_style

        )
    )

    story.append(
        Paragraph(

            f"The product validation score was "
            f"<b>{score}/100</b>.",

            body_style

        )
    )

    story.append(
        Paragraph(

            f"The generated recommendation was: "
            f"<b>{safe_text(recommendation)}</b>.",

            body_style

        )
    )

    story.append(
        Paragraph(

            "The report combines synthetic persona "
            "profiles, response analysis, theme clusters, "
            "sentiment, key persona quotes and AI-generated "
            "research insights into one structured research "
            "artifact.",

            body_style

        )
    )

    # =====================================================
    # BUILD PDF
    # =====================================================

    document.build(

        story,

        onFirstPage=add_page_number,

        onLaterPages=add_page_number

    )