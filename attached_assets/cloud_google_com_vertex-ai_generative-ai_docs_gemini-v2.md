URL: https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2#2.0-flash-lite
---
[Skip to main content](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2#main-content)

[![Google Cloud](https://www.gstatic.com/devrel-devsite/prod/v38a693baeb774512feb42f10aac8f755d8791ed41119b5be7a531f8e16f8279f/cloud/images/cloud-logo.svg)](https://cloud.google.com/)

`/`

- [English](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2#2.0-flash-lite)
- [Deutsch](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2?hl=de#2.0-flash-lite)
- [Español – América Latina](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2?hl=es-419#2.0-flash-lite)
- [Français](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2?hl=fr#2.0-flash-lite)
- [Indonesia](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2?hl=id#2.0-flash-lite)
- [Italiano](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2?hl=it#2.0-flash-lite)
- [Português – Brasil](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2?hl=pt-br#2.0-flash-lite)
- [中文 – 简体](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2?hl=zh-cn#2.0-flash-lite)
- [日本語](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2?hl=ja#2.0-flash-lite)
- [한국어](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2?hl=ko#2.0-flash-lite)

[Sign in](https://cloud.google.com/_d/signin?continue=https%3A%2F%2Fcloud.google.com%2Fvertex-ai%2Fgenerative-ai%2Fdocs%2Fgemini-v2%232.0-flash-lite&prompt=select_account)

- [Generative AI](https://cloud.google.com/vertex-ai/generative-ai/docs/overview)

[Contact Us](https://cloud.google.com/contact) [Start free](https://console.cloud.google.com/freetrial)

- On this page
- [2.0 models](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2#20_models)
- [Google Gen AI SDK](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2#google-gen)
  - [(Optional) Set environment variables](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2#env-vars)

- [Home](https://cloud.google.com/)
- [Generative AI](https://cloud.google.com/vertex-ai/generative-ai/docs/overview)
- [Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/overview)

Was this helpful?



 Send feedback



# Gemini 2.0

bookmark\_borderbookmark

 Stay organized with collections


 Save and categorize content based on your preferences.


Release Notes


- On this page
- [2.0 models](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2#20_models)
- [Google Gen AI SDK](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2#google-gen)
  - [(Optional) Set environment variables](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2#env-vars)

The Gemini 2.0 models are the latest Google models supported in
Vertex AI. This page goes over the following models:

- [Gemini 2.0 Flash](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2#2.0-flash)
- [Gemini 2.0 Flash-Lite](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2#2.0-flash-lite)
- [Gemini 2.0 Pro](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2#2.0-pro)

If you're looking for information on our
Gemini 2.0 Flash Thinking model, visit our [Gemini 2.0 Flash Thinking documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/thinking).

## 2.0 models

[2.0 Flash](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2#2.0-flash)[2.0 Flash-Lite](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2#2.0-flash-lite)[2.0 Pro](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2#2.0-pro)More

Gemini 2.0 Flash is our latest generally available model in
the Gemini family. It's our workhorse model for all daily tasks and
features enhanced performance and supports real-time Live API. 2.0 Flash is
an upgrade path for 1.5 Flash users who want a slightly slower model with
significantly better quality, or 1.5 Pro users who want slightly better
quality and real-time latency for less.

Gemini 2.0 Flash introduces the following new and enhanced
features:

- **Multimodal Live API:** This new API enables low-latency bidirectional
voice and video interactions with Gemini.
- **Quality:** Enhanced performance across most quality benchmarks than
Gemini 1.5 Pro.
- **Improved agentic capabilities:** 2.0 Flash delivers improvements to
multimodal understanding, coding, complex instruction following, and
function calling. These improvements work together to support better agentic
experiences.
- **New modalities:** 2.0 Flash introduces built-in image generation and
controllable text-to-speech capabilities, enabling image editing, localized
artwork creation, and expressive storytelling.

Gemini 2.0 Flash features:

- Multimodal input
- Text output (general availability) / multimodal output (private preview)
- Prompt optimizers
- Controlled generation
- Function calling
- Grounding with Google Search
- Code execution
- Count token

Use this model ID to use Gemini 2.0 Flash with the [Gen AI SDK](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2#google-gen): `gemini-2.0-flash-001`

### Feature availability

The following features are available for Gemini 2.0 Flash:

| Feature | Availability level |
| --- | --- |
| [Text generation](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/send-chat-prompts-gemini) | Generally available |
| [Grounding with Google Search](https://cloud.google.com/vertex-ai/generative-ai/docs/grounding-with-search) | Generally available |
| [Gen AI SDK](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2#google-gen) | Generally available |
| [Multimodal Live API](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal-live-api) | Public preview |
| [Bounding box detection](https://cloud.google.com/vertex-ai/generative-ai/docs/bounding-box-detection) | Public preview |
| [Image generation](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal-response-generation#image-generation) | Private preview |
| [Speech generation](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal-response-generation#speech-generation) | Private preview |

- **Generally available:** This feature is available publicly and supported
for use in production-level code.
- **Public preview:** This feature is available publicly in a reduced
capacity. Don't use features that are released as a public preview in
production code, because the support level and functionality of that feature
can change without warning.
- **Private preview:** This feature is only available to users listed on an
approved allow-list. Don't use features that are released as a private
preview in production code, because the support level and functionality of
that feature can change without warning.

### Pricing

Information on the pricing for Gemini 2.0 Flash is available
on our [Pricing page](https://cloud.google.com/vertex-ai/generative-ai/pricing).

### Quotas and limitations

GA features in Gemini 2.0 Flash uses [dynamic shared\\
quota](https://cloud.google.com/vertex-ai/generative-ai/docs/dsq).

Grounding with Google Search in Gemini 2.0 Flash is subject
to [rate limiting](https://cloud.google.com/vertex-ai/generative-ai/pricing#modality-based-pricing).

Gemini 2.0 Flash-Lite is our fastest and most cost efficient
Flash model. It's an upgrade path for 1.5 Flash users who want better quality
for the same price and speed.

Gemini 2.0 Flash-Lite includes:

- Multimodal input, text output
- 1M token input context window
- 8k token output context window

2.0 Flash-Lite **does not** include the
following 2.0 Flash features:

- Multimodal output generation
- Integration with Multimodal Live API
- Thinking mode
- Built-in tool usage

Use this model ID to use Gemini 2.0 Flash-Lite with the [Gen AI SDK](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2#google-gen): `gemini-2.0-flash-lite-preview-02-05`

### Quotas and limitations

Gemini 2.0 Flash-Lite is rate limited to 60 queries per
minute during Public Preview.

Gemini 2.0 Flash-Lite is only available in the
`us-central1` region in Vertex AI.

Gemini 2.0 Pro is our strongest model for coding and world
knowledge and features a 2M long context window.
Gemini 2.0 Pro is available as an experimental model in
Vertex AI and is an upgrade path for 1.5 Pro users who want better
quality, or who are particularly invested in long context and code.

Gemini 2.0 Pro features:

- Multimodal input
- Text output
- Prompt optimizers
- Controlled generation
- Function calling (excluding compositional function calling)
- Grounding with Google Search
- Code execution
- Count token

Use this model ID to use Gemini 2.0 Pro with the [Gen AI SDK](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2#google-gen): `gemini-2.0-pro-exp-02-05`

### Quotas and limitations

Gemini 2.0 Pro is rate limited to 10 queries per minute
(QPM) during Experimental.

Grounding with Google Search in Gemini 2.0 Pro is subject
to [rate limiting](https://cloud.google.com/vertex-ai/generative-ai/pricing#modality-based-pricing).

## Google Gen AI SDK

The Gen AI SDK provides a unified interface to Gemini 2.0
through both the Gemini Developer API and the Gemini API on
Vertex AI. With a few exceptions, code that runs on one platform will
run on both. This means that you can prototype an application using the
Developer API and then migrate the application to Vertex AI without
rewriting your code.

The Gen AI SDK also supports the Gemini 1.5 models.

The SDK is generally available in Python. Support for Go is in Preview, and
Java and JavaScript support is coming soon.

You can start using the SDK as shown.

[Gen AI SDK for Python](https://cloud.google.com/vertex-ai/generative-ai/docs/gemini-v2#gen-ai-sdk-for-python)More

Learn how to install or update the [Google Gen AI SDK for Python](https://cloud.google.com/vertex-ai/generative-ai/docs/sdks/overview).



For more information, see the
[Gen AI SDK for Python API reference documentation](https://googleapis.github.io/python-genai/) or the
[`python-genai` GitHub repository](https://googleapis.github.io/python-genai/).



Set environment variables to use the Gen AI SDK with Vertex AI:

See more code actions.

Light code theme

Dark code theme

```
# Replace the `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION` values
# with appropriate values for your project.
export GOOGLE_CLOUD_PROJECT=GOOGLE_CLOUD_PROJECT
export GOOGLE_CLOUD_LOCATION=us-central1
export GOOGLE_GENAI_USE_VERTEXAI=True
```

See more code actions.

[Open in Editor](https://shell.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&cloudshell_open_in_editor=/genai/text_generation/textgen_with_txt.py) [View on GitHub](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/HEAD/genai/text_generation/textgen_with_txt.py)

Light code theme

Dark code theme

Send feedback

```
from google import genai
from google.genai.types import HttpOptions

client = genai.Client(http_options=HttpOptions(api_version="v1"))
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents="How does AI work?",
)
print(response.text)
# Example response:
# Okay, let's break down how AI works. It's a broad field, so I'll focus on the ...
#
# Here's a simplified overview:
# ...
```

### (Optional) Set environment variables

Alternatively, you can initialize the client using environment variables. First
set the appropriate values and export the variables:

See more code actions.

Light code theme

Dark code theme

```
# Replace the `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION` values
# with appropriate values for your project.
export GOOGLE_CLOUD_PROJECT=YOUR_CLOUD_PROJECT
export GOOGLE_CLOUD_LOCATION=us-central1
export GOOGLE_GENAI_USE_VERTEXAI=True

```

Then you can initialize the client without any args:

See more code actions.

Light code theme

Dark code theme

```
client = genai.Client()

```

Was this helpful?



 Send feedback



Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-02-14 UTC.

[iframe](https://scone-pa.clients6.google.com/static/proxy.html?usegapi=1&jsh=m%3B%2F_%2Fscs%2Fabc-static%2F_%2Fjs%2Fk%3Dgapi.lb.en.5oZHy0SiJxw.O%2Fd%3D1%2Frs%3DAHpOoo-Hry6DG-RE4t9kNz_t6hiwmwXOmA%2Fm%3D__features__#parent=https%3A%2F%2Fcloud.google.com&rpctoken=309801336)