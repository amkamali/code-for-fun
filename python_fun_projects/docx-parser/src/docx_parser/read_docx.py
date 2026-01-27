import argparse
from docx import Document
from pathlib import Path
from docx.oxml import OxmlElement
from docx.text.paragraph import Paragraph


def rewrite_profile_section(docx_path: str, new_texts: list[str], output_path: str):
    """
    Replaces the paragraphs in profile section of a DOCX file,
    preserving the original formatting of those paragraphs.
    args:
        docx_path (str): Path to the input DOCX file.
        new_texts (list[str]): A list of the new texts to replace the paragraphs between profile and core competencies.
        output_path (str): Path to save the modified DOCX file.
    returns:
        None
    """
    doc = Document(docx_path)

    def _copy_font(dst_font, src_font):
        if src_font is None:
            return
        try:
            dst_font.name = src_font.name
            dst_font.size = src_font.size
            dst_font.bold = src_font.bold
            dst_font.italic = src_font.italic
            dst_font.underline = src_font.underline
            if getattr(src_font, "color", None) is not None:
                dst_font.color.rgb = src_font.color.rgb
        except Exception:
            # Best-effort copy; ignore attributes not set
            pass

    for i, paragraph in enumerate(doc.paragraphs):
        if (
            paragraph.style.name == "Heading 1"
            and paragraph.text.lower().strip() == "profile"
        ):
            # Determine the next Heading 1 that marks the end (Core Competencies)
            j = None
            for idx, next_paragraph in enumerate(doc.paragraphs[i + 1 :], start=i + 1):
                if (
                    next_paragraph.style.name == "Heading 1"
                    and next_paragraph.text.lower().strip() == "core competencies"
                ):
                    j = idx
                    break
            if j is None:
                # No end heading found; nothing to rewrite
                break

            # Preserve style and run formatting from the first body paragraph after "Profile"
            sample_paragraph = (
                doc.paragraphs[i + 1] if i + 1 < len(doc.paragraphs) else None
            )
            sample_style = (
                sample_paragraph.style if sample_paragraph is not None else None
            )
            sample_run_font = (
                sample_paragraph.runs[0].font
                if (sample_paragraph is not None and sample_paragraph.runs)
                else None
            )

            # Delete paragraphs between Profile and Core Competencies (exclusive)
            for idx in range(j - 1, i, -1):
                p = doc.paragraphs[idx]
                p._element.getparent().remove(p._element)

            # Insert new paragraphs directly after the Profile heading
            anchor = doc.paragraphs[i]  # Profile heading paragraph
            insert_after = anchor
            for text in new_texts:
                new_p = OxmlElement("w:p")
                insert_after._p.addnext(new_p)
                new_para = Paragraph(new_p, anchor._parent)
                if sample_style is not None:
                    new_para.style = sample_style
                run = new_para.add_run(text)
                _copy_font(run.font, sample_run_font)
                insert_after = new_para

            doc.save(output_path)
            return


def main():
    """
    Command-line interface to replace paragraph after a specified heading in a DOCX file.
    args:
        None
    returns:
        None
    """
    parser = argparse.ArgumentParser(
        description="Replace paragraph after heading in a DOCX file."
    )
    parser.add_argument(
        "docx_path",
        type=Path,
        default="../sample_document.docx",
        help="Path to the input DOCX file",
    )
    parser.add_argument(
        "new_text_path",
        type=str,
        help="Path to the text file containing new text for profile section",
    )
    parser.add_argument(
        "output_path",
        type=Path,
        default="../new_sample_document.docx",
        help="Path to save the modified DOCX file",
    )
    args = parser.parse_args()

    with open(args.new_text_path, "r") as f:
        new_text = f.read().strip().split("\n")

    rewrite_profile_section(
        docx_path=args.docx_path, new_texts=new_text, output_path=args.output_path
    )


if __name__ == "__main__":
    main()
