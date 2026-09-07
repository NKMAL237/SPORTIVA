import io
import os
from django.conf import settings
from django.core.files.base import ContentFile
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


def generate_event_invoice_pdf(registration):
    """
    Generates a high-resolution, branded SPORTIVA Digital Invoice & Event Entry Ticket PDF.
    Returns bytes content of the PDF.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom Brand Styles
    brand_dark = colors.HexColor('#0F172A')
    brand_blue = colors.HexColor('#0EA5E9')
    brand_emerald = colors.HexColor('#10B981')
    brand_slate = colors.HexColor('#334155')
    text_dark = colors.HexColor('#1E293B')
    text_muted = colors.HexColor('#64748B')
    bg_light = colors.HexColor('#F8FAFC')
    border_color = colors.HexColor('#E2E8F0')

    title_style = ParagraphStyle(
        'InvoiceTitle',
        parent=styles['Heading1'],
        fontSize=24,
        leading=28,
        textColor=brand_dark,
        fontName='Helvetica-Bold'
    )
    subtitle_style = ParagraphStyle(
        'InvoiceSubtitle',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        textColor=brand_blue,
        fontName='Helvetica-Bold'
    )
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=12,
        leading=16,
        textColor=brand_dark,
        fontName='Helvetica-Bold'
    )
    body_style = ParagraphStyle(
        'InvoiceBody',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=text_dark,
        fontName='Helvetica'
    )
    body_bold = ParagraphStyle(
        'InvoiceBodyBold',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=text_dark,
        fontName='Helvetica-Bold'
    )
    small_style = ParagraphStyle(
        'InvoiceSmall',
        parent=styles['Normal'],
        fontSize=8,
        leading=11,
        textColor=text_muted,
        fontName='Helvetica'
    )

    elements = []

    # 1. Header Banner
    header_data = [
        [
            Paragraph("<b>SPORTIVA</b><br/><font color='#0EA5E9' size='8'>GLOBAL SPORTS NETWORK & TALENT PLATFORM</font>", title_style),
            Paragraph(f"<b>OFFICIAL INVOICE & ENTRY PASS</b><br/>Invoice #: <font color='#0EA5E9'><b>{registration.invoice_number}</b></font><br/>Date: {registration.registered_at.strftime('%B %d, %Y')}<br/>Status: <font color='#10B981'><b>{registration.get_payment_status_display()}</b></font>", body_style)
        ]
    ]
    header_table = Table(header_data, colWidths=[3.2 * inch, 4.0 * inch])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 15))
    elements.append(HRFlowable(width="100%", thickness=2, color=brand_blue, spaceBefore=1, spaceAfter=15))

    # 2. Billing & Event Overview (2 Columns)
    user = registration.user
    event = registration.event
    
    billing_info = [
        Paragraph("<b>BILLED TO (PARTICIPANT / ATHLETE)</b>", heading_style),
        Paragraph(f"<b>Name:</b> {user.get_full_name() or user.username}", body_style),
        Paragraph(f"<b>Username / ID:</b> @{user.username} (ID: #{user.id})", body_style),
        Paragraph(f"<b>Email:</b> {user.email}", body_style),
        Paragraph(f"<b>Location:</b> {user.city}, {user.country}", body_style),
        Paragraph(f"<b>Role / Tier:</b> {user.get_role_display()}", body_style),
    ]

    event_info = [
        Paragraph("<b>EVENT & TOURNAMENT DETAILS</b>", heading_style),
        Paragraph(f"<b>Event:</b> {event.title}", body_style),
        Paragraph(f"<b>Sport:</b> {event.sport.name} ({event.category.name})", body_style),
        Paragraph(f"<b>Venue:</b> {event.venue_name}, {event.city}, {event.country}", body_style),
        Paragraph(f"<b>Start Date:</b> {event.start_date.strftime('%A, %B %d, %Y at %H:%M UTC')}", body_style),
        Paragraph(f"<b>Organizer:</b> {event.organizer.username} ({event.organization.name if event.organization else 'Sportiva Official'})", body_style),
    ]

    info_data = [[billing_info, event_info]]
    info_table = Table(info_data, colWidths=[3.6 * inch, 3.6 * inch])
    info_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (-1, -1), bg_light),
        ('BOX', (0, 0), (-1, -1), 1, border_color),
        ('INNERGRID', (0, 0), (-1, -1), 1, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 20))

    # 3. Itemized Receipt Table
    fee_str = f"{registration.amount_paid:,} {registration.currency}" if registration.amount_paid > 0 else "FREE ENTRY"
    items_data = [
        [
            Paragraph("<b>Item Description</b>", body_bold),
            Paragraph("<b>Registration Code</b>", body_bold),
            Paragraph("<b>Payment Method</b>", body_bold),
            Paragraph("<b>Amount</b>", body_bold)
        ],
        [
            Paragraph(f"<b>Official Event Entry & Pass:</b><br/>{event.title}<br/><font color='#64748B' size='7.5'>Includes digital athlete accreditation, score logging & merit verification rights.</font>", body_style),
            Paragraph(f"<code>{str(registration.registration_code)[:18]}...</code>", small_style),
            Paragraph(f"{registration.payment_method}", body_style),
            Paragraph(f"<b>{fee_str}</b>", body_bold)
        ],
        [
            "", "",
            Paragraph("<b>Total Paid:</b>", body_bold),
            Paragraph(f"<b><font color='#10B981' size='11'>{fee_str}</font></b>", body_bold)
        ]
    ]

    items_table = Table(items_data, colWidths=[3.2 * inch, 1.6 * inch, 1.2 * inch, 1.2 * inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), brand_dark),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, 0), 2, brand_blue),
        ('BACKGROUND', (0, 1), (-1, 1), colors.white),
        ('BACKGROUND', (0, 2), (-1, 2), bg_light),
    ]))
    elements.append(items_table)
    elements.append(Spacer(1, 20))

    # 4. Security Stamp & Organizer Verification Box
    security_data = [
        [
            Paragraph("<b>DIGITAL SECURITY & VALIDATION STAMP</b><br/>"
                      f"Pass Code: <b>{str(registration.registration_code)[:24]}</b><br/>"
                      f"Organizer Verification: <font color='#10B981'><b>{'VALIDATED & ROSTERED' if registration.organizer_validated else 'PENDING CHECK-IN'}</b></font><br/>"
                      "Show this digital PDF pass upon venue arrival or present your Sportiva mobile QR code.", body_style),
            Paragraph("<b>SPORTIVA VERIFIED TRANSACTION</b><br/>"
                      "<font size='8' color='#10B981'>✔ Digitally Signed & Authenticated</font><br/>"
                      f"<font size='7' color='#64748B'>Timestamp: {registration.registered_at.isoformat()}</font>", body_style)
        ]
    ]
    sec_table = Table(security_data, colWidths=[4.4 * inch, 2.8 * inch])
    sec_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F0FDF4')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#86EFAC')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(sec_table)
    elements.append(Spacer(1, 25))

    # 5. Footer
    elements.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceBefore=5, spaceAfter=8))
    footer_text = Paragraph(
        "<font size='7' color='#94A3B8'>SPORTIVA — Universal Sports Network & Global Tournament Management Platform.<br/>"
        "Questions regarding this invoice or event access? Contact support@sportiva.app or message the event organizer on SPORTIVA Chat.</font>",
        small_style
    )
    elements.append(footer_text)

    # Build PDF
    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
