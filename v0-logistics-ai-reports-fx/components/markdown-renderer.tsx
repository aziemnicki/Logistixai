interface MarkdownRendererProps {
  content: string
}

export function MarkdownRenderer({ content }: MarkdownRendererProps) {
  // Convert markdown to HTML
  const renderMarkdown = (text: string) => {
    let html = text

    // Headers
    html = html.replace(/^### (.*$)/gim, '<h3 class="font-semibold text-base mt-3 mb-2">$1</h3>')
    html = html.replace(/^## (.*$)/gim, '<h2 class="font-semibold text-lg mt-4 mb-2">$1</h2>')
    html = html.replace(/^# (.*$)/gim, '<h1 class="font-bold text-xl mt-4 mb-3">$1</h1>')

    // Bold
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong class="font-semibold">$1</strong>')
    html = html.replace(/__(.+?)__/g, '<strong class="font-semibold">$1</strong>')

    // Italic
    html = html.replace(/\*(.+?)\*/g, '<em class="italic">$1</em>')
    html = html.replace(/_(.+?)_/g, '<em class="italic">$1</em>')

    // Code blocks
    html = html.replace(
      /```([\s\S]*?)```/g,
      '<pre class="bg-muted p-2 rounded my-2 overflow-x-auto"><code>$1</code></pre>',
    )

    // Inline code
    html = html.replace(/`(.+?)`/g, '<code class="bg-muted px-1 py-0.5 rounded text-sm">$1</code>')

    // Links
    html = html.replace(
      /\[([^\]]+)\]$$([^)]+)$$/g,
      '<a href="$2" class="text-primary underline hover:no-underline" target="_blank" rel="noopener noreferrer">$1</a>',
    )

    // Unordered lists
    html = html.replace(/^\* (.+)$/gim, '<li class="ml-4">• $1</li>')
    html = html.replace(/^- (.+)$/gim, '<li class="ml-4">• $1</li>')

    // Ordered lists
    html = html.replace(/^\d+\. (.+)$/gim, '<li class="ml-4 list-decimal">$1</li>')

    // Line breaks
    html = html.replace(/\n\n/g, "<br/><br/>")
    html = html.replace(/\n/g, "<br/>")

    return html
  }

  return <div className="prose prose-sm max-w-none" dangerouslySetInnerHTML={{ __html: renderMarkdown(content) }} />
}
