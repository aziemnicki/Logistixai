from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, Flowable
)
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from datetime import datetime
import os
import json


# --- FONT REGISTRATION (Inter, IBM Plex Sans) ---
def register_fonts():
    """Register custom fonts with proper path resolution and fallback handling."""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    fonts_to_register = [
        ('IBMPlexSans', 'IBMPlexSans_SemiCondensed-ExtraLightItalic.ttf'),
        ('IBMPlexSans-Bold', 'IBMPlexSans_SemiCondensed-BoldItalic.ttf'),
        ('Inter-Bold', 'Inter_18pt-Bold.ttf'),
        ('Inter-SemiBold', 'Inter_18pt-SemiBold.ttf'),
        ('Inter-Medium', 'Inter_18pt-Medium.ttf'),
    ]

    registered_fonts = []
    missing_fonts = []

    print("\n🔤 Font Registration:")
    for font_name, font_file in fonts_to_register:
        # Build absolute path to font file
        font_path = os.path.join(script_dir, font_file)

        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont(font_name, font_path))
                registered_fonts.append(font_name)
                print(f"   ✓ {font_name}: {font_file}")
            except Exception as e:
                print(f"   ✗ {font_name}: Failed to register - {e}")
                missing_fonts.append(font_name)
        else:
            print(f"   ✗ {font_name}: File not found at {font_path}")
            missing_fonts.append(font_name)

    if registered_fonts:
        print(f"   ✅ Successfully registered {len(registered_fonts)}/{len(fonts_to_register)} fonts")

    if missing_fonts:
        print(f"   ⚠️  {len(missing_fonts)} fonts unavailable, will use fallback (Helvetica)")
        print(f"   📝 Missing: {', '.join(missing_fonts)}")

    return registered_fonts, missing_fonts

# Register fonts and track which ones are available
_registered_fonts, _missing_fonts = register_fonts()

# Helper function to get safe font name with fallback
def get_font_name(preferred_font, fallback='Helvetica'):
    """Get font name with fallback if preferred font is not registered."""
    if preferred_font in _registered_fonts:
        return preferred_font
    else:
        # Map to appropriate Helvetica variant
        if 'Bold' in preferred_font:
            return 'Helvetica-Bold'
        return fallback

class PDFReportGenerator:
    """Generate professional PDF reports from compliance data."""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        def add_style(style_name, parent_name=None, **kwargs):
            try:
                if style_name in self.styles:
                    return self.styles[style_name]
                parent = None
                if parent_name:
                    try:
                        parent = self.styles[parent_name]
                    except KeyError:
                        parent = self.styles.get('Normal', None)
                style = ParagraphStyle(name=style_name, parent=parent, **kwargs)
                self.styles.add(style)
                return style
            except Exception as e:
                print(f"Error creating style '{style_name}': {e}")
                fallback_styles = list(self.styles.byName.keys())
                return self.styles.get('Normal', self.styles[fallback_styles[0]])

        # Set base font for body text (IBM Plex Sans for regular text)
        self.styles['Normal'].fontName = get_font_name('IBMPlexSans', 'Helvetica')
        self.styles['BodyText'].fontName = get_font_name('IBMPlexSans', 'Helvetica')

        # Heading styles with Inter font
        add_style('CustomTitle', parent_name='Heading1', fontSize=20, leading=24, alignment=TA_CENTER,
                  textColor=colors.HexColor('#1a365d'), spaceAfter=30, spaceBefore=10,
                  fontName=get_font_name('Inter-Bold', 'Helvetica-Bold'))

        add_style('SectionHeader', parent_name='Heading1', fontSize=14, leading=18,
                  textColor=colors.HexColor('#2c3e50'), spaceAfter=12, spaceBefore=24,
                  fontName=get_font_name('Inter-Bold', 'Helvetica-Bold'))

        add_style('Section', parent_name='Heading2', fontSize=12, textColor=colors.HexColor('#2c3e50'),
                  spaceAfter=12, spaceBefore=12,
                  fontName=get_font_name('Inter-SemiBold', 'Helvetica-Bold'))

        add_style('SubSection', parent_name='Heading3', fontSize=11, textColor=colors.HexColor('#4a4a4a'),
                  spaceAfter=6, spaceBefore=6,
                  fontName=get_font_name('Inter-Medium', 'Helvetica-Bold'))

        # Risk level styles with IBMPlexSans-Bold
        for level, color in [('Critical', '#d32f2f'), ('High', '#f57c00'),
                             ('Medium', '#fbc02d'), ('Low', '#388e3c')]:
            add_style(f'Risk{level}', parent_name='BodyText', fontSize=10,
                      textColor=colors.HexColor(color),
                      fontName=get_font_name('IBMPlexSans-Bold', 'Helvetica-Bold'))

    def generate_pdf(self, report_data, output_path, sources=None):
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        doc = SimpleDocTemplate(
            output_path, pagesize=letter, rightMargin=72, leftMargin=72,
            topMargin=72, bottomMargin=18
        )
        story = []
        story.extend(self._create_header(report_data))
        story.extend(self._create_summary_section(report_data))
        story.extend(self._create_legal_changes_section(report_data))
        story.extend(self._create_route_impacts_section(report_data))
        story.extend(self._create_actions_section(report_data))
        if sources:
            story.extend(self._create_sources_section(sources))
        story.extend(self._create_footer(report_data))
        doc.build(story)
        print(f"✓ PDF generated: {output_path}")

    def _create_header(self, report_data):
        elements = []
        # -- IMAGE PLACEHOLDER --
        logo_path = 'logo.jpg'  # <- replace this with your logo file path if needed
        img_height = 0.6 * inch
        img_width = img_height  # square

        try:
            img = Image(logo_path, width=img_width, height=img_height)
            img.hAlign = 'LEFT'
            logo_element = img
        except Exception:
            from reportlab.graphics.shapes import Drawing, Rect, String
            class Placeholder(Flowable):
                def __init__(self, width, height):
                    Flowable.__init__(self)
                    self.width = width
                    self.height = height
                def draw(self):
                    self.canv.setStrokeColor(colors.lightgrey)
                    self.canv.setFillColor(colors.whitesmoke)
                    self.canv.rect(0, 0, self.width, self.height, fill=1)
                    self.canv.setFillColor(colors.grey)
                    self.canv.setFont("Helvetica", 8)
                    self.canv.drawString(2, self.height/2-4, "Logo")
            logo_element = Placeholder(img_width, img_height)

        from reportlab.platypus import Table
        # Title placed next to image
        title_para = Paragraph(
            "Logistics Compliance Report",
            self.styles.get('CustomTitle', self.styles['Heading1'])
        )
        title_table = Table(
            [[logo_element, title_para]],
            colWidths=[img_width + 8, 5 * inch],
            style=[('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]
        )
        elements.append(title_table)
        elements.append(Spacer(1, 0.2 * inch))

        company_name = report_data.get('company_name', 'Unknown Company')
        generated_at = report_data.get('generated_at', datetime.utcnow().isoformat())
        report_id = report_data.get('id', 'N/A')
        try:
            date_obj = datetime.fromisoformat(generated_at.replace('Z', '+00:00'))
            formatted_date = date_obj.strftime('%B %d, %Y at %H:%M UTC')
        except Exception:
            formatted_date = generated_at
        info_data = [
            ['Company:', company_name],
            ['Report ID:', report_id],
            ['Generated:', formatted_date],
        ]
        info_table = Table(info_data, colWidths=[1.5 * inch, 4.5 * inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'IBMPlexSans-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'IBMPlexSans'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#4a4a4a')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#333333')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 0.4 * inch))
        return elements

    def _create_summary_section(self, report_data):
        elements = []
        content = report_data.get('content', {})
        summary = content.get('summary', {})
        elements.append(Paragraph("Executive Summary", 
            self.styles.get('SectionHeader', self.styles['Heading1'])))
        total_changes = summary.get('total_changes', 0)
        overall_risk = summary.get('overall_risk', 'medium').title()
        risk_color = self._get_risk_color(summary.get('overall_risk', 'medium'))
        summary_data = [
            ['Total Changes Identified:', str(total_changes)],
            ['Overall Risk Level:', overall_risk],
        ]
        summary_table = Table(summary_data, colWidths=[2.5 * inch, 3.5 * inch])
        summary_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'IBMPlexSans-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'IBMPlexSans'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#4a4a4a')),
            ('TEXTCOLOR', (1, 1), (1, 1), risk_color),
            ('FONTNAME', (1, 1), (1, 1), 'IBMPlexSans-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.grey),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.2 * inch))
        takeaways = summary.get('key_takeaways', [])
        if takeaways:
            elements.append(Paragraph("Key Takeaways:", self.styles.get('SubSection', self.styles['Heading3'])))
            for takeaway in takeaways:
                bullet = Paragraph(f"• {takeaway}", self.styles['BodyText'])
                elements.append(bullet)
        elements.append(Spacer(1, 0.3 * inch))
        return elements

    def _create_legal_changes_section(self, report_data):
        elements = []
        content = report_data.get('content', {})
        legal_changes = content.get('legal_changes', [])
        if not legal_changes:
            return elements
        elements.append(Paragraph("Legal & Regulatory Changes", 
            self.styles.get('SectionHeader', self.styles['Heading1'])))
        elements.append(Spacer(1, 0.1 * inch))
        for idx, change in enumerate(legal_changes, 1):
            title = change.get('title', 'Untitled Change')
            risk_level = change.get('risk_level', 'medium').title()
            risk_style_name = f"Risk{risk_level}"
            risk_style = self.styles.get(risk_style_name, self.styles['BodyText'])
            elements.append(Paragraph(f"{idx}. {title}", 
                self.styles.get('SubSection', self.styles['Heading3'])))
            elements.append(Paragraph(f"Risk Level: {risk_level}", risk_style))
            description = change.get('description', 'No description available')
            elements.append(Paragraph(description, self.styles['BodyText']))
            countries = change.get('affected_countries', [])
            if countries:
                elements.append(Paragraph(
                    f"<b>Affected Countries:</b> {', '.join(countries)}",
                    self.styles['BodyText']
                ))
            effective_date = change.get('effective_date')
            if effective_date:
                elements.append(Paragraph(
                    f"<b>Effective Date:</b> {effective_date}",
                    self.styles['BodyText']
                ))
            source_url = change.get('source_url', '')
            if source_url:
                elements.append(Paragraph(
                    f'<b>Source:</b> <link href="{source_url}">{source_url}</link>',
                    self.styles['BodyText']
                ))
            elements.append(Spacer(1, 0.2 * inch))
        return elements

    def _create_route_impacts_section(self, report_data):
        elements = []
        content = report_data.get('content', {})
        route_impacts = content.get('route_impacts', [])
        if not route_impacts:
            return elements
        elements.append(PageBreak())
        elements.append(Paragraph("Route-Specific Impacts",
            self.styles.get('SectionHeader', self.styles['Heading1'])))
        elements.append(Spacer(1, 0.1 * inch))
        for idx, impact in enumerate(route_impacts, 1):
            route_name = impact.get('route_name', 'Unknown Route')
            risk_level = impact.get('risk_level', 'medium').title()
            risk_style_name = f"Risk{risk_level}"
            risk_style = self.styles.get(risk_style_name, self.styles['BodyText'])
            elements.append(Paragraph(f"{idx}. {route_name}", 
                self.styles.get('SubSection', self.styles['Heading3'])))
            elements.append(Paragraph(f"Risk Level: {risk_level}", risk_style))
            description = impact.get('impact_description', 'No description')
            elements.append(Paragraph(description, self.styles['BodyText']))
            actions = impact.get('recommended_actions', [])
            if actions:
                elements.append(Paragraph("<b>Recommended Actions:</b>", self.styles['BodyText']))
                for action in actions:
                    elements.append(Paragraph(f"• {action}", self.styles['BodyText']))
            elements.append(Spacer(1, 0.2 * inch))
        return elements

    def _create_actions_section(self, report_data):
        elements = []
        content = report_data.get('content', {})
        actions = content.get('recommended_actions', [])
        if not actions:
            return elements
        elements.append(PageBreak())
        elements.append(Paragraph("Recommended Actions",
            self.styles.get('SectionHeader', self.styles['Heading1'])))
        elements.append(Spacer(1, 0.1 * inch))
        actions_by_priority = {}
        for action in actions:
            priority = action.get('priority', 'medium')
            if priority not in actions_by_priority:
                actions_by_priority[priority] = []
            actions_by_priority[priority].append(action)
        for priority in ['critical', 'high', 'medium', 'low']:
            if priority not in actions_by_priority:
                continue
            priority_actions = actions_by_priority[priority]
            risk_style_name = f"Risk{priority.title()}"
            risk_style = self.styles.get(risk_style_name, self.styles['BodyText'])
            elements.append(Paragraph(f"{priority.upper()} PRIORITY", risk_style))
            elements.append(Spacer(1, 0.05 * inch))
            for action in priority_actions:
                action_text = action.get('action', 'No action specified')
                deadline = action.get('deadline')
                if deadline:
                    elements.append(Paragraph(
                        f"• {action_text} <b>(Deadline: {deadline})</b>", self.styles['BodyText']))
                else:
                    elements.append(Paragraph(f"• {action_text}", self.styles['BodyText']))
            elements.append(Spacer(1, 0.15 * inch))
        return elements

    def _create_sources_section(self, sources):
        elements = []
        if not sources:
            return elements
        elements.append(PageBreak())
        elements.append(Paragraph("Sources & References",
            self.styles.get('SectionHeader', self.styles['Heading1'])))
        elements.append(Spacer(1, 0.1 * inch))
        for idx, source in enumerate(sources, 1):
            title = source.get('title', 'Untitled')
            url = source.get('url', '')
            snippet = source.get('snippet', '')
            elements.append(Paragraph(f"{idx}. <b>{title}</b>", self.styles['BodyText']))
            if snippet:
                snippet_text = snippet[:200] + ('...' if len(snippet) > 200 else '')
                elements.append(Paragraph(snippet_text, self.styles['BodyText']))
            if url:
                elements.append(Paragraph(f'<link href="{url}">{url}</link>', self.styles['BodyText']))
            elements.append(Spacer(1, 0.1 * inch))
        return elements

    def _create_footer(self, report_data):
        elements = []
        elements.append(PageBreak())
        elements.append(Spacer(1, 0.5 * inch))
        iteration_count = report_data.get('iteration_count', 1)
        status = report_data.get('status', 'unknown')
        model = report_data.get('model', 'AI Technology')
        footer_text = f"""
        <para align=center fontSize=8 textColor=#666666>
        This report was generated automatically by the Logistics Compliance AI System.<br/>
        Report Status: {status.title()} | Validation Iterations: {iteration_count}<br/>
        Generated with {model}<br/>
        <br/>
        For questions or concerns, please contact your compliance team.
        </para>
        """
        elements.append(Paragraph(footer_text, self.styles['BodyText']))
        return elements

    def _get_risk_color(self, risk_level):
        colors_map = {
            'critical': colors.HexColor('#d32f2f'),
            'high': colors.HexColor('#f57c00'),
            'medium': colors.HexColor('#fbc02d'),
            'low': colors.HexColor('#388e3c')
        }
        return colors_map.get(risk_level.lower(), colors.black)


# Global PDF service instance
pdf_service = PDFReportGenerator()


def get_pdf_service() -> PDFReportGenerator:
    """Get the global PDF service instance."""
    return pdf_service


# =====================
# MAIN SCRIPT SECTION
# =====================

if __name__ == "__main__":
    # EDIT THIS LINE to your input/output file names:
    json_input_path = r"C:\Users\PozMI\Desktop\hackathon\\Logistic_simple\\data\\reports\\7eb99686-bc73-4ef3-99a9-886fbb50fdd0.json"     # <-- change to your file name
    pdf_output_path = r"C:\Users\PozMI\Desktop\hackathon\\Logistic_simple\\data\\reports\\pdfs\\7eb99686-bc73-4ef3-99a9-886fbb50fdd0_v2.pdf"    # <-- change as needed

    # Optional: sources section, supply as Python list if you want
    # sources = [ {'title': '...', 'url': '...', 'snippet': '...'}, ... ]
    sources = None

    # Load data and generate PDF
    with open(json_input_path, "r", encoding="utf-8") as f:
        report_data = json.load(f)

    pdf_gen = PDFReportGenerator()
    pdf_gen.generate_pdf(report_data, pdf_output_path, sources)
