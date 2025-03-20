import { NextResponse } from "next/server";
import openai from "openai";
import fs from "fs/promises";
import { encoding_for_model } from "tiktoken";


export async function GET(req) {
  console.log("Scraping latest news/articles...");

  let response = await fetch("http://127.0.0.1:5000/scrape", {
    method: "GET",
    timeout: 120000,
  });
  let data = await response.json();

  let final_articles = [];

  for (let i = 0; i < data.length; i++) {
    let content = data[i]["article_content"];
    let meta_data = data[i]["article"];
    if (content.length > 1300) {
      final_articles.push({
        content: content.slice(0, 1000) + content.slice(-300),
        meta_data: meta_data,
      });
    } else {
      final_articles.push({
        content: content,
        meta_data: meta_data,
      });
    }
  }

  console.log("The data fetched from scraper: ", final_articles);

  if (final_articles) {
    console.log("Prompting LLM...");

    const openai = require("openai");

    // Instantiate the OpenAI client
    const client = new openai({
      apiKey: process.env.OPENAI_API_KEY,
    });

    const hardcodedPrompt = `
    I’m building an AI-powered tool to generate content ideas for LinkedIn posts and short-form scripts based on recent news. The content should be relevant to professionals and industry-specific, capturing insights, trends, or actionable takeaways. Consider the context preferences provided below to tailor each idea to the tone, style, and content preferences best suited for LinkedIn.

    Context Preferences:

    Audience: {Business professionals, industry leaders, technical recruiters, fellow tech students, software engineers, data engineers, AI engineers and tech enthusiasts}

    Audience industry domains: {Professional Services, IT Services and IT Consulting, Software Development}

    Tone: {Informative, concise, insightful, and engaging}

    Style: Focus on real-world applications, leadership insights, and emerging trends

    Length: Short, punchy posts (around 900-1000 words for LinkedIn)

    Key Goals: Boost engagement, prompt discussion, highlight innovation, and provide value to readers

    Structure recommendations for the output:{
    
    effective structure:

    Compelling Hook: Begin with a strong opening line to grab attention. This could be a provocative question, a surprising statement, or a bold opinion related to your field.

    Personal Insight or Story: Share a personal experience or observation. This makes your post relatable and authentic, allowing readers to connect with you on a deeper level.

    Minimal Facts for Context: Include brief factual information or data to provide context or support your insight. Keep this section concise to maintain focus on your personal narrative.

    Unique Takeaways: Conclude with new, insightful takeaways or lessons learned from your experience. Offer a fresh perspective or actionable advice that readers can apply.

    Engagement Prompt: End with a question or call-to-action that encourages readers to share their thoughts or experiences in the comments.

    Example Structure:"

    Hook: "Innovation isn't always about creating something new—sometimes, it's about seeing the familiar in a new light."

    Personal Insight: "Recently, I revisited an old project that I'd shelved years ago. With fresh eyes and experiences, I discovered potential I hadn't seen before. It taught me the value of reflection and reassessment."

    Minimal Fact: "In fact, many successful products are iterations of earlier concepts that were ahead of their time."

    Takeaway: "Don't dismiss past ideas too quickly. Revisiting them might reveal opportunities that align perfectly with today's needs."

    Engagement Prompt: "Have you ever rediscovered value in an old idea? I'd love to hear your stories."
    "
    potential_categories = [AI, Start-up, Cybersecurity, Block Chain, Media, Social, Hardware, Software, Space, Health, Climate, Technology, Fin-tech, Government, Apps, Entertainment"]
    VERY IMPORTANT NOTE: PLEASE GENERATE RESPONSE IN AN ARRAY OF OBJECTS, WITH EACH ITEM AS AN IDEA. The response shouldn't contain anything except the array, starting with '[' and ending with ']'. DO not include any sort of headings or endings in the response. 
    Example structure of response: [
    {
    hook: "title or hook of the post, very eye-catchy" ,
    body: "the rest of the post content",
    category: "refer to the potential_categories list given in the prompt and choose the one best fits the article body.,
    },
    {
    hook: "title or hook of the post, very eye-catchy" ,
    body: "the rest of the post content",
    category: "refer to the potential_categories list given in the prompt and choose the one best fits the article body.,
    },..
    ]
    Based on the above context and content, generate 8-10 LinkedIn posts in JSON format. If 10 articles/news are given, generate atleast 1 linkedin posts for each.
    
    Main Content of real-time fetched news = Content: ${JSON.stringify(final_articles)}
    `;
    const functions = [
      {
        name: "generate_linkedin_ideas",
        description: "Generates LinkedIn posts based on the latest news articles provided.",
        parameters: {
          type: "object",
          properties: {
            ideas: {
              type: "array",
              description: "An array of LinkedIn post ideas.",
              items: {
                type: "object",
                properties: {
                  hook: {
                    type: "string",
                    description: "Title or hook of the post, less than 30-40 words, eye-catchy.",
                  },
                  body: {
                    type: "string",
                    description: "The rest of the post content. Approx 1000 words for each idea",
                  },
                  body: {
                    type: "string",
                    description: "The category.",
                  },
                },
                required: ["hook", "body", "category"],
              },
            },
          },
          required: ["ideas"],
        },
      },
    ];

    // Initialize the tokenizer for GPT-3.5 Turbo
    const { encoding_for_model } = require("tiktoken");
    const tokenizer = encoding_for_model("gpt-3.5-turbo");
    const maxTokens = 4096;
    const reservedOutputTokens = 1000;
    const availableInputTokens = maxTokens - reservedOutputTokens;
    
    // Calculate token usage for static messages
    const staticMessages = [
      { role: "system", content: "You are an AI agent who generates Linkedin Posts from provided articles/news/blogs." },
    ];
    
    const staticTokenCount = staticMessages.reduce(
      (total, message) => total + tokenizer.encode(message.content).length,
      0
    );
    console.log("staticTokenCount: ", staticTokenCount);
    
    const remainingTokensForPrompt = availableInputTokens - staticTokenCount;
    console.log("remainingTokensForPrompt: ", remainingTokensForPrompt);
    
    // Truncate the prompt if necessary
    let truncatedPrompt = hardcodedPrompt;
    const promptTokens = tokenizer.encode(hardcodedPrompt).length;
    console.log("actual promptTokens: ", promptTokens);
    
    if (promptTokens > remainingTokensForPrompt) {
      // Simply truncate to 13,000 characters
      truncatedPrompt = hardcodedPrompt.slice(0, 13000);
      console.log("Prompt truncated to first 13,000 characters.");
    }
    
    console.log("Final prompt to send:", truncatedPrompt);
    

    // Construct input messages
    const inputMessages = [
      ...staticMessages,
      {
        role: "user",
        content: truncatedPrompt,
      },
    ];

    // Call the OpenAI API
    try {
      const completion = await client.chat.completions.create({
        model: "gpt-3.5-turbo",
        messages: inputMessages,
        functions: functions,
        function_call: { name: "generate_linkedin_ideas" },
      });

      const response_from_llm = completion.choices[0].message;

      // Access the token usage information
      const inputTokens = completion.usage.prompt_tokens;
      const outputTokens = completion.usage.completion_tokens;
      const totalTokens = completion.usage.total_tokens;

      console.log("Input Tokens (Prompt):", inputTokens);
      console.log("Output Tokens (Completion):", outputTokens);
      console.log("Total Tokens Used:", totalTokens);

      if (response_from_llm.function_call) {
        const functionArgs = response_from_llm.function_call.arguments;
        try {
          const ideas = JSON.parse(functionArgs).ideas;
          console.log("Parsed ideas:", ideas);
          return NextResponse.json({ body: ideas });
        } catch (error) {
          console.error("Error parsing function arguments:", error);
          return NextResponse.json({ body: [] });
        }
      } else {
        console.error("No function call in the response");
        return NextResponse.json({ body: [] });
      }
    } catch (error) {
      console.error("Error calling OpenAI API:", error);
      return NextResponse.json({ body: [] });
    }
  } else {
    console.error("No data received from the scraper");
    return NextResponse.json({ body: [] });
  }
}





