from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

def create_presentation(content: dict) -> Presentation:
    """
    Creates a PowerPoint presentation from a dictionary of content.

    Args:
        content: A dictionary with 'title_slide', 'content_slides', and 'final_slide'.

    Returns:
        A python-pptx Presentation object.
    """
    
    # Create a new presentation (uses default built-in template)
    # You could also load a template: prs = Presentation('templates/default_template.pptx')
    prs = Presentation()
    
    # --- 1. Add Title Slide ---
    try:
        title_slide_layout = prs.slide_layouts[0] # Title slide layout
        slide = prs.slides.add_slide(title_slide_layout)
        title = slide.shapes.title
        subtitle = slide.placeholders[1]
        
        title.text = content.get("title_slide", {}).get("title", "Missing Title")
        subtitle.text = content.get("title_slide", {}).get("subtitle", "Missing Subtitle")
    except Exception as e:
        print(f"Error creating title slide: {e}")

    # --- 2. Add Content Slides ---
    try:
        content_slide_layout = prs.slide_layouts[1] # Title and Content layout
        
        for content_slide in content.get("content_slides", []):
            slide = prs.slides.add_slide(content_slide_layout)
            title_shape = slide.shapes.title
            body_shape = slide.placeholders[1]
            
            title_shape.text = content_slide.get("title", "Missing Slide Title")
            
            tf = body_shape.text_frame
            tf.clear() # Clear existing text
            
            # Set top-level bullet point
            p = tf.paragraphs[0]
            p.text = content_slide.get("content", [])[0] if content_slide.get("content") else ""
            p.font.size = Pt(24)
            
            # Add subsequent bullet points
            for bullet_point in content_slide.get("content", [])[1:]:
                p = tf.add_paragraph()
                p.text = bullet_point
                p.font.size = Pt(24)
                p.level = 0 # You can use levels 1, 2, etc. for indentation
                
    except Exception as e:
        print(f"Error creating content slides: {e}")

    # --- 3. Add Final Slide ---
    try:
        final_slide_layout = prs.slide_layouts[0] # Use Title layout for simplicity
        slide = prs.slides.add_slide(final_slide_layout)
        
        title = slide.shapes.title
        subtitle = slide.placeholders[1]

        final_content = content.get("final_slide", {})
        title.text = final_content.get("title", "Thank You")
        
        # Center the title text
        title.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        
        # Use subtitle for content
        subtitle.text = "\n".join(final_content.get("content", ["Questions?"]))
        subtitle.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        
    except Exception as e:
        print(f"Error creating final slide: {e}")

    return prs
