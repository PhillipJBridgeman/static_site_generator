import unittest
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_links,
    extract_markdown_images,
    text_to_textnodes,
)

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode(
            "This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_empty_old_nodes(self):
        result = split_nodes_delimiter([], "*", text_type_text)
        self.assertEqual(result, [])

    def test_delimiter_not_found(self):
        node = TextNode("This is just a sentence", text_type_text)
        result = split_nodes_delimiter([node], "*", text_type_text)
        self.assertEqual(result, [node])

    def test_closing_delimiter_not_found_italic(self):
        node = TextNode("This is a *test sentence", text_type_text)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", text_type_italic)

    def test_closing_delimiter_not_found_code(self):
        node = TextNode("This is a `test sentence", text_type_text)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", text_type_code)

    def test_no_images(self):
        text = "This is a text without any images"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_single_image(self):
        text = "This is a text with a single image ![alt text](https://example.com/image.jpg)"
        result = extract_markdown_images(text)
        self.assertEqual(
            result, [("alt text", "https://example.com/image.jpg")])

    def test_multiple_images(self):
        text = "This is a text with multiple images ![alt1](https://example.com/image1.jpg) and ![alt2](https://example.com/image2.jpg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [
                         ("alt1", "https://example.com/image1.jpg"), ("alt2", "https://example.com/image2.jpg")])

    def test_no_alt_text(self):
        text = "This is a text with an image that has no alt text ![]https://example.com/image.gif)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_no_image_link(self):
        text = "This is a text with an image that has no image link ![alt text]"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_multiple_links(self):
        text = "This is a [link](https://example.com) and [another link](https://another.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [
                         ("link", "https://example.com"), ("another link", "https://another.com")])

    def test_no_links(self):
        text = "This is a text without any links"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_single_link(self):
        text = "This is a [single link](https://singlelink.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("single link", "https://singlelink.com")])

    def test_links_with_different_text_and_urls(self):
        text = "Here is a [link](https://example.com) and [another link](https://another.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [
                         ("link", "https://example.com"), ("another link", "https://another.com")])

    def test_empty_old_nodes(self):
        result = split_nodes_image([])
        self.assertEqual(result, [])

    def test_no_images(self):
        node = TextNode("This is a text without any images", text_type_text)
        result = split_nodes_image([node])
        self.assertEqual(result, [node])

    def test_single_image(self):
        node = TextNode(
            "This is text with an ![image](https://www.example.com/image.png)", text_type_text)
        expected_nodes = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image,
                     "https://www.example.com/image.png")
        ]
        result = split_nodes_image([node])
        self.assertEqual(result, expected_nodes)

    def test_multiple_images(self):
        node = TextNode(
            "This is text with an ![image1](https://www.example.com/image1.png) and ![image2](https://www.example.com/image2.png)", text_type_text)
        expected_nodes = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image1", text_type_image,
                     "https://www.example.com/image1.png"),
            TextNode(" and ", text_type_text),
            TextNode("image2", text_type_image,
                     "https://www.example.com/image2.png")
        ]
        result = split_nodes_image([node])
        self.assertEqual(result, expected_nodes)

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image,
                         "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", text_type_image,
                         "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_no_links(self):
        node = TextNode("This is a text without links", text_type_text)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node])

    def test_single_link(self):
        node = TextNode(
            "This is a text with a [single link](https://example.com)", text_type_text)
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("This is a text with a ", text_type_text),
            TextNode("single link", text_type_link, "https://example.com")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_multiple_links(self):
        node = TextNode(
            "Text with [link1](https://link1.com) and [link2](https://link2.com)", text_type_text)
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("Text with ", text_type_text),
            TextNode("link1", text_type_link, "https://link1.com"),
            TextNode(" and ", text_type_text),
            TextNode("link2", text_type_link, "https://link2.com")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode("another link", text_type_link,
                         "https://blog.boot.dev"),
                TextNode(" with text that follows", text_type_text),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("image", text_type_image,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ],
            nodes,
        )


if __name__ == "__main__":
    unittest.main()