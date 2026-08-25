# Weekly report technology section

Use this pattern when the user asks for a technology section about AI, agents, or model news inside a report/doc.

## Default structure
1. Research current items from official sources first.
2. Present **alternatives** before adding any text to the doc.
3. Keep each entry short:
   - short title
   - one-line context if needed
   - URL reference
4. Prefer 3-5 items max unless the user asks for more.

## Preferred sources
- OpenAI News RSS: `https://openai.com/news/rss.xml`
- Google AI blog RSS: `https://blog.google/technology/ai/rss/`
- Anthropic news sitemap: `https://www.anthropic.com/sitemap.xml`
- Official product/blog pages for the vendor in question

## What to avoid
- Self-referential phrasing in the report entry
- Long summaries when the user asked for links/ref titles
- Adding a final entry before showing candidate alternatives when the user asked to choose first

## Good output shape
| Option | Title | URL |
|---|---|---|
| A | The next evolution of the Agents SDK | https://openai.com/index/the-next-evolution-of-the-agents-sdk |
| B | Gemini 3.5: frontier intelligence with action | https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5/ |
| C | Claude Opus 4.8 | https://www.anthropic.com/news/claude-opus-4-8 |
