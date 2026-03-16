from xml.etree import ElementTree as ET


def parse_xml(file_path):
    """解析XML文件，提取 keyword 或 keypoint 属性
    返回列表，每个元素是 (类型, 值) 的元组，类型为 'keyword' 或 'keypoint'
    """
    results = []
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # 查找所有 rec_paper 标签
        for rec_paper in root.findall(".//rec_paper"):
            # 支持 keyword 和 keywords 两种属性名
            keyword = rec_paper.attrib.get("keyword") or rec_paper.attrib.get("keywords")
            keypoint = rec_paper.attrib.get("keypoint") or rec_paper.attrib.get("keypoints")

            # 返回元组 (类型, 值)
            if keyword:
                results.append(("keyword", keyword))
            if keypoint:
                results.append(("keypoint", keypoint))
    except ET.ParseError as e:
        results.append(("error", f"解析XML错误: {e}"))
    except Exception as e:
        results.append(("error", f"处理文件时发生错误: {e}"))
    
    return results
