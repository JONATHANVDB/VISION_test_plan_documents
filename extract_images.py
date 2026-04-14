import docx
import os

def extract_images(docx_path, out_dir):
    doc = docx.Document(docx_path)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    img_count = 0
    for rel in doc.part.rels.values():
        if "image" in rel.target_ref:
            img_count += 1
            ext = rel.target_ref.split('.')[-1]
            img_name = f"image_{img_count}.{ext}"
            with open(os.path.join(out_dir, img_name), "wb") as f:
                f.write(rel.target_part.blob)
    print(f"Extracted {img_count} images from {docx_path} to {out_dir}")

if __name__ == "__main__":
    files = [
        "Projects/VISION_test_plan_documents/test plans/IMG002x1_test_plan_1v2.docx",
        "Projects/VISION_test_plan_documents/test plans/mag-cxp-product-test-plan_1v2.docx",
        "Projects/VISION_test_plan_documents/test plans/MAG_VIS100XX_EVK_Modules_Test_Plan.docx",
        "Projects/VISION_test_plan_documents/test plans/ProductTestDevelopmentMAG-PSU_test_plan_1v2.docx"
    ]
    for f in files:
        out_dir = f + "_images"
        extract_images(f, out_dir)
