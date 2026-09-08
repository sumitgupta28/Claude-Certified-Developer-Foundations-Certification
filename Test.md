
--- QUIZ ---

Topic: 1 MSO Foundations

1. A fintech startup runs Claude 3.5 Haiku in zero-shot mode to auto-tag support tickets, and the JSON schema compliance rate sits at 82%, below the 95% target defined in evals. The team is deciding whether to escalate to Sonnet or add worked examples to the Haiku prompt. Which action reflects the evaluation-driven methodology taught in MSO Foundations?

* A) Immediately switch every ticket to Claude Opus zero-shot to guarantee compliance regardless of cost.

* B) Add 2–3 targeted multi-shot examples demonstrating the exact JSON schema on Haiku, then re-run the eval suite before considering a model upgrade.

* C) Increase `temperature` to 1.0 on Haiku so the model explores more diverse token paths.

* D) Disable the eval suite since string-matching tests already confirmed model correctness.

2. During a load test, a batch of prompts collectively exceeds the model's context window before generation begins. Separately, another long-running generation is cut off mid-response after consuming the full window. How should the engineering team differentiate these two situations in their error handling code?

* A) Treat both as the same `stop_reason` and apply identical retry logic.

* B) The first case returns an immediate API validation error prior to generation; the second returns a truncated response with a context-exceeded stop reason mid-turn, requiring different handling paths.

* C) Both cases silently truncate the oldest conversation turns automatically.

* D) Both cases require lowering `top_p` to recover the missing tokens.

3. A QA engineer argues that because Claude produced two differently worded but equally correct answers to the identical prompt across two test runs, the model is "broken." What is the technically accurate explanation and appropriate fix for the automated test suite?

* A) The API experienced a caching bug; the fix is to clear the prompt cache before each test.

* B) This is expected non-determinism from autoregressive sampling; the suite should assert on structural/semantic properties or use a model-graded judge rather than exact string equality.

* C) The model's context window overflowed silently; the fix is to reduce `max_tokens`.

* D) The tokenizer randomly dropped punctuation; the fix is to strip whitespace before comparison.

4. An architecture team is deciding between running an entire pipeline on Claude Opus with reasoning always on, versus a tiered approach. Historical data shows 90% of requests are simple classification tasks and 10% require deep multi-step legal reasoning. Which design is most consistent with the model-tiering principles in MSO Foundations?

* A) Run 100% of traffic on Opus with high reasoning effort to avoid any risk of quality loss.

* B) Run 100% of traffic on Haiku with reasoning disabled to minimize cost regardless of accuracy on the 10% complex slice.

* C) Route the 90% classification slice to a fast, low-cost tier and escalate the 10% complex slice to a high-capability tier with higher reasoning effort, validated by evals.

* D) Alternate models randomly per request to average out cost and quality across the traffic mix.

5. A developer needs Claude's output fed directly into a downstream SQL execution engine with zero tolerance for conversational preamble text. Simply telling the model "return only SQL, no explanation" in the prompt has proven unreliable in production. What is the most robust architectural fix?

* A) Increase `top_k` to force the model toward more literal token choices.

* B) Enforce a strict Tool Use JSON schema (or structured output) so the SQL argument is returned in a validated parameter field rather than freeform text.

* C) Post-process the raw text response with a regex that strips the first sentence.

* D) Switch to one-shot prompting only, since multi-shot prompting cannot constrain output format.

6. A team benchmarks the exact same extraction task using zero-shot prompting on Sonnet versus multi-shot prompting (3 examples) on Haiku. Both configurations pass the eval suite at 96% accuracy, but Haiku with examples costs 70% less per call. According to the composable model/prompting-mode framework, what does this result demonstrate?

* A) Multi-shot prompting fine-tunes the underlying Haiku weights, permanently improving its capability.

* B) Worked examples let a cheaper, smaller model match a more capable model's zero-shot structural accuracy, making it the more cost-effective production choice.

* C) Zero-shot prompting is strictly forbidden on high-capability models per Anthropic's API policy.

* D) The eval suite results are invalid because they used two different model tiers.

7. An engineering team is deciding between synchronous, streaming, and asynchronous batch execution for three separate features: (1) a live in-app chat assistant, (2) a nightly bulk re-summarization of 200,000 archived tickets, and (3) a backend microservice that returns a short structured verdict with no UI. Which pairing is correct?

* A) Chat → batch; nightly job → streaming; backend verdict → synchronous.

* B) Chat → streaming (SSE); nightly job → Message Batches API; backend verdict → synchronous request/response.

* C) Chat → synchronous; nightly job → synchronous with threading; backend verdict → streaming.

* D) All three should use the Message Batches API to simplify the codebase.

8. A Python backend service handling concurrent live user queries currently blocks its event loop on every Claude API call, causing request queuing under load. Which SDK-level change directly resolves this without altering the model or prompting strategy?

* A) Switch to the TypeScript SDK's `AsyncAnthropic` class, since Python lacks native async support.

* B) Refactor to use the Python SDK's `AsyncAnthropic` client with `async/await` so the thread isn't blocked during network I/O.

* C) Increase `max_tokens` so each call returns faster.

* D) Move all calls to the Message Batches API to eliminate blocking entirely, even for real-time chat.

9. A developer disables all sampling randomness (`temperature=0.0`, tightly restricted `top_p`) for a financial data-extraction feature and still occasionally observes minor wording differences in surrounding narrative text, though the extracted numeric fields remain stable. What is the most accurate interpretation?

* A) This indicates a bug in the API, since `temperature=0.0` should guarantee byte-for-byte identical output every time.

* B) Lowering temperature reduces variance by biasing generation toward high-probability tokens, but does not mathematically guarantee zero variance; tests should still assert on structural/numeric invariants rather than exact prose.

* C) The context window silently truncated the system prompt.

* D) The tokenizer non-deterministically re-splits words on every call.

10. A one-off internal script needs to summarize a single support ticket exactly once, with no reuse across turns and no future scaling requirements. Which prompting-mode and transport combination best fits the "minimal sufficiency" discipline described in MSO Foundations?

* A) Multi-shot prompting with 5 examples over a persistent streaming connection.

* B) Zero-shot prompting with a synchronous, non-streamed request.

* C) One-shot prompting routed through the Message Batches API with a 24-hour SLA.

* D) Multi-shot prompting combined with extended thinking at maximum effort.

11. A team observes that a prompt asking Claude to output data in a specific nested JSON structure with custom enum values fails intermittently even after lengthening the instructional text describing the schema. According to the module's guidance on output shape versus instructions, what is the most effective next step?

* A) Continue expanding the instructional paragraph describing the schema in even greater detail.

* B) Add 1–2 concrete worked examples showing the exact nested JSON and enum values, since descriptive text alone often cannot pin down precise output shape.

* C) Remove the system prompt entirely so the model relies purely on user-turn context.

* D) Raise `temperature` to 1.0 to give the model more freedom to infer the correct structure.

---

Topic: 2 Production-Grade Prompting, Agents & Tool Use

1. An agent that queries an internal database tool starts returning multi-megabyte JSON blobs into the conversation, and after 6 turns the session begins hitting `stop_reason: model_context_window_exceeded`. The team wants a fix that doesn't require switching model tiers. What should they implement?

* A) Increase `max_tokens` on every subsequent call so the model can finish its response.

* B) Filter, truncate, or summarize the raw tool output at the application layer before it re-enters the model's context window.

* C) Enable extended thinking so Claude internally compresses the tool output.

* D) Convert the tool's `input_schema` from JSON Schema to XML to reduce token overhead.

2. During a multi-turn agent session using extended thinking, a developer strips out old `thinking` blocks before sending the next turn to save context tokens. The very next API call fails. What is the root cause and the correct remedy?

* A) The API rejects the request because thinking blocks carry cryptographic signatures that must be returned unmodified in every subsequent turn; the developer must restore the full untouched blocks instead of trimming them.

* B) The API silently regenerates the missing reasoning at no extra cost, so this is actually a safe optimization.

* C) The failure is unrelated to thinking blocks; it is caused by the `effort` parameter being deprecated.

* D) Thinking blocks are optional metadata and can always be safely dropped without consequence.

3. A banking agent has two tools registered: `check_balance` (read-only) and `wire_transfer` (state-changing, irreversible). What architectural pattern must gate execution of `wire_transfer` specifically, beyond what the tool's JSON schema alone can enforce?

* A) A stricter `input_schema` with additional required fields on `wire_transfer`.

* B) A Human-in-the-Loop (HITL) checkpoint requiring explicit user/administrator approval before the transfer tool actually executes.

* C) Removing the `check_balance` tool so the model has fewer choices to confuse.

* D) Setting `disable_parallel_tool_use: true` on the API request.

4. While consuming a streamed response containing a `tool_use` block, an engineer's client code begins calling `json.loads()` on each `content_block_delta` fragment as it arrives, hoping to start the tool execution early. This throws repeated parsing exceptions. What is the correct streaming pattern?

* A) Buffer the partial JSON fragments in memory and only attempt to parse/execute after the corresponding `content_block_stop` event fires.

* B) Wrap every delta in a try/except and silently ignore parsing failures.

* C) Switch off streaming entirely, since tool use is fundamentally incompatible with SSE.

* D) Parse only the final delta fragment and discard all preceding ones.

5. Two tools, `get_customer_profile` and `get_customer_billing`, have overlapping semantic descriptions, and Claude frequently invokes the wrong one when asked about billing history. Renaming schema fields hasn't helped. What is the most effective remediation?

* A) Merge both tools into one with 20 optional parameters to reduce ambiguity.

* B) Add explicit inclusion and exclusion criteria to each tool's description (e.g., "use this when... do not use this when...") to disambiguate routing.

* C) Set `strict: true` on both tools so Claude is forced to guess correctly.

* D) Remove the `description` field from both tools to force reliance on the tool name alone.

6. An enterprise team wants to connect Claude Code to a proprietary internal system exposed only via a locally spawned binary process (no network listener) using the Anthropic API's MCP Connector. After configuration, connections consistently fail. What is the architectural reason?

* A) The API MCP Connector only supports remote servers over Streamable HTTP; local `stdio` servers must be managed client-side, not through the API connector.

* B) The internal binary must first be rewritten in Python to be MCP-compatible.

* C) `stdio` transport requires a paid enterprise MCP license unavailable in this configuration.

* D) MCP servers can only expose Resources, not Tools, over `stdio`.

7. A production agent must summarize a single long PDF, and the finance team is asking why the pipeline sends the entire document as a rasterized set of images instead of using a dedicated document ingestion path. What is the correct fix?

* A) Keep sending images, since PDFs are not supported by the Messages API in any other form.

* B) Pass the PDF using the `document` content block type rather than converting pages to `image` blocks, preserving native layout and reducing unnecessary visual-token overhead.

* C) Convert the PDF to a `.txt` file locally and paste the raw text into the system prompt.

* D) Use the Message Batches API exclusively, since document blocks are unsupported outside batch mode.

8. A subagent spawned mid-session to handle an isolated code-review task fails to apply the coding standards defined by a Skill actively loaded in the parent session. What is the underlying architectural rule being encountered?

* A) Subagents automatically inherit all parent skills; this must be an unrelated bug.

* B) Subagents start with a clean context window and do not automatically inherit parent skills or conversation history — required skills must be explicitly declared on the subagent.

* C) Skills can only be loaded by the top-level orchestrator and never by any delegated process.

* D) The Skill file must be renamed to match the subagent's name exactly to be inherited.

9. An architecture review flags that a customer support workflow implemented as a rigid, fully-enumerable sequence of steps was instead built as an autonomous multi-tool agent, resulting in unpredictable execution order and higher token costs with no accuracy benefit. What was the correct architectural choice from the outset?

* A) An Agent, because agents are always superior to workflows regardless of task shape.

* B) A Workflow, because the steps could be enumerated in code, inputs were well-constrained, and strict guardrails/observability were achievable without emergent tool sequencing.

* C) A Claude Managed Agent, because server-side hosting always reduces token costs.

* D) A subagent-only architecture with no orchestrator.

10. A healthcare startup wants to minimize infrastructure maintenance by using Claude Managed Agents for a PHI-handling patient intake workflow. What compliance constraint must the architecture team account for?

* A) Managed Agents automatically satisfy HIPAA BAA requirements because Anthropic manages the servers.

* B) Managed Agents store stateful sessions server-side and are currently ineligible for HIPAA BAA or Zero Data Retention coverage, requiring the Agent SDK or a raw API loop on a BAA-covered configuration instead.

* C) HIPAA compliance is only a concern for the Messages API, not for agent runtimes.

* D) Managed Agents can be made HIPAA-compliant simply by enabling `bypassPermissions`.

11. A 20-turn troubleshooting session repeatedly re-sends a large architecture diagram as an inline Base64 image block in every user turn. Token costs and latency have grown noticeably. What change would most directly address this without losing the ability to reference the image?

* A) Convert the image to a `document` content block type instead.

* B) Upload the image once via the Files API (or a stable URL reference) and reference it across turns instead of re-transmitting the full Base64 payload every turn.

* C) Reduce `max_tokens` on every turn to compensate for the image size.

* D) Enable `disable_parallel_tool_use` to offset the image's token cost.

---

Topic: 3 Claude Code, MCP & Integration

1. An enterprise wants critical infrastructure directories protected even if an individual developer's machine is switched into `bypassPermissions` mode during a demo. Which control guarantees this protection regardless of local developer settings?

* A) A `plan` mode instruction placed in the project's `README.md`.

* B) Path-level deny rules defined in enterprise `managed-settings.json`, since deny rules deterministically override allow rules and bypass modes at every configuration tier.

* C) Asking developers to manually confirm before every file edit.

* D) Relying solely on `acceptEdits` mode to block risky paths.

2. A plugin author hardcodes an absolute path like `/Users/jdoe/projects/tool-config.json` inside a shared Skill distributed via an internal plugin marketplace. Teammates report the plugin fails immediately upon install. What is the root cause?

* A) The plugin marketplace only supports relative URLs, not file paths.

* B) The Skill embeds a local, machine-specific absolute path instead of a project-relative path, breaking portability across teammates' machines.

* C) `SKILL.md` files cannot contain any file path references at all.

* D) The plugin needs `disable-model-invocation: true` to resolve paths correctly.

3. A team commits a project-scoped `.mcp.json` using `stdio` transport so the whole team can "share" one running server instance. After cloning the repo, most teammates get connection failures while a few succeed. What's the actual behavior of this configuration?

* A) `stdio` transport creates one shared remote server that all clones connect to; failures indicate a network firewall issue only.

* B) `stdio` spawns a separate local subprocess on each individual machine; failures occur on machines lacking the required local runtime (e.g., Node/npx) to launch that subprocess.

* C) `.mcp.json` files are ignored unless registered in enterprise `managed-settings.json`.

* D) `stdio` transport requires an active internet connection to function, unlike HTTP transport.

4. A developer discovers an API token was hardcoded in `.mcp.json`, commits a fix replacing it with `${API_TOKEN}`, and considers the incident closed. A security reviewer disagrees. Why?

* A) Environment variable interpolation doesn't work inside `.mcp.json` files, so the fix is technically broken.

* B) The original token remains permanently recoverable from earlier commits in git history; the token must be rotated/revoked, not just replaced in the latest commit.

* C) `.mcp.json` automatically encrypts all string values on commit, making the concern moot.

* D) Only OAuth tokens require rotation; static API keys are exempt from this rule.

5. A `CLAUDE.md` file has grown to include architecture diagrams, a full changelog, database rules, and style guides. Developers notice Claude increasingly ignores the test-driven-development rule stated at the top of the file. What is the most likely cause and fix?

* A) `/init` must be re-run to refresh file priorities.

* B) Context window dilution — the oversized file reduces the relative weight of any single rule; large or specialized content should move into path-scoped rules files or on-demand Skills, keeping `CLAUDE.md` concise.

* C) `CLAUDE.md` has a hard 4KB limit and is silently truncating content.

* D) The TDD rule must be moved into a `PostToolUse` hook to be enforced.

6. A team wants deterministic enforcement — not just a polite instruction — that Claude Code can never delete files inside `src/config/production/`, even during complex multi-step refactors. Which mechanism actually guarantees this?

* A) Writing "Never delete production config files" at the top of `CLAUDE.md`.

* B) A `PreToolUse` hook that inspects the target file path before deletion and exits with code 2 (blocking execution) when the path matches the protected directory.

* C) Placing a rules file inside a subdirectory named `production/` inside `.claude/rules/`.

* D) Relying on the `Explore` subagent to never suggest destructive changes.

7. An MCP server exposing 40 database tools causes noticeable prompt token bloat before any user interaction even begins. Which configuration change directly reduces this upfront context cost?

* A) Setting `disable_parallel_tool_use: true` on every request.

* B) Setting `defer_loading: true` within the `mcp_toolset` default configuration so full tool definitions load into context only when needed.

* C) Renaming all 40 tools to shorter identifiers.

* D) Switching the MCP transport from HTTP to `stdio`.

8. A federal agency requiring FedRAMP High authorization asks a vendor to deploy a Claude-powered analysis tool. The vendor proposes "Claude Enterprise via AWS Marketplace." Why does this fail compliance review?

* A) AWS Marketplace listings are never usable by federal agencies under any authorization.

* B) Claude Enterprise on AWS Marketplace is explicitly not FedRAMP authorized; only Bedrock GovCloud, C4G via Palantir, or GCP Vertex AI Assured Workloads satisfy this requirement.

* C) FedRAMP High requires the first-party Anthropic Console, which the vendor didn't propose.

* D) FedRAMP authorization only applies to Managed Agents, not direct API usage.

9. During a compliance audit, a reviewer wants an immutable, model-independent record of every file modification an agent performed during a modernization project. Which mechanism satisfies this requirement, and why?

* A) A `PreToolUse` hook, because it runs before execution and can therefore log intent.

* B) A `PostToolUse` hook, because it fires deterministically after execution, capturing exact parameters into an external log that the model itself cannot alter or skip.

* C) The `Explore` subagent's built-in transcript, since it always includes a full audit trail.

* D) The `CLAUDE.md` file, since all rules are logged automatically by Claude Code.

10. A code review pipeline flags two issues: (1) a missing null check clearly visible in the diff, and (2) a claim that the change "will likely cause a deadlock under high concurrency" with no supporting evidence. How should the team weigh these two findings?

* A) Reject the PR automatically based on both findings since AI-generated reviews are authoritative.

* B) Trust the null-check finding since it's directly verifiable from the diff; treat the deadlock claim as an unproven hypothesis requiring empirical testing before acting on it.

* C) Ignore both findings since AI code review cannot be trusted for security-relevant changes.

* D) Automatically apply a fix for the deadlock claim while ignoring the null-check finding.

11. A developer wants a database-migration workflow that must NEVER trigger automatically based on Claude's interpretation of a user's request — only an explicit `/db-migrate` command should ever run it. How should the Skill be configured?

* A) Omit the `description` field entirely from the Skill's frontmatter.

* B) Set `disable-model-invocation: true` in the Skill's YAML frontmatter so it can only be triggered via explicit slash command.

* C) Store the Skill inside `.claude/commands/` instead of `.claude/skills/`.

* D) Set `plan` mode as the default permission mode for the entire project.

---

Topic: 4 Production Engineering, Evals & Security

1. An LLM-as-a-judge pipeline is consistently assigning high scores to customer support summaries that omit critical details or hallucinate transaction IDs. What must the team do before trusting this judge in a production gate?

* A) Lower the judge model's temperature to 0 and consider the problem solved.

* B) Calibrate the judge's rubric and scoring behavior against a set of human-labeled ground truth examples to verify agreement and eliminate bias before relying on it for deployment decisions.

* C) Replace the LLM judge entirely with exact string-match assertions on summary length.

* D) Increase the judge model's `max_tokens` so it can write longer justifications.

2. A document-processing service encounters an HTTP 429 during peak load and, separately, an "Invalid Context Length" error on an oversized upload. The on-call engineer wants one unified retry policy for both. Why is this the wrong approach?

* A) Both errors are permanent and neither should ever be retried.

* B) The 429 is a transient, retriable failure suited to exponential backoff, while the context-length error is a terminal, structural failure that will fail identically on every retry and must instead trigger a fallback (e.g., chunking or truncation) rather than blind retries.

* C) Both errors should be retried immediately in a tight loop without backoff to minimize latency.

* D) HTTP 429 errors should always be treated as terminal since rate limits rarely clear.

3. A research agent with a web-browsing tool suddenly stops summarizing a target article and instead attempts to transmit the system prompt's contents to an external endpoint referenced inside the fetched page. What vulnerability occurred and what is the architectural fix?

* A) This is a direct jailbreak; fixed by enabling prompt caching.

* B) This is an indirect prompt injection, where malicious instructions were embedded in untrusted external content; the fix is to enforce strict boundaries treating all fetched content as untrusted data and restrict the tool's action scope.

* C) This is a schema validation failure; fixed by adding `strict: true` to the browsing tool.

* D) This is a context window overflow; fixed by increasing `max_tokens`.

4. A multi-agent pipeline spawns four parallel subagents to analyze single-sentence user queries, and monthly telemetry shows a 6x cost increase with degraded latency compared to a single-agent baseline, without any measurable accuracy gain. What is the correct remediation per production engineering guidance?

* A) Add a fifth subagent to further parallelize the workload.

* B) Instrument per-call token/latency metrics and collapse the architecture back to a single agent, reserving parallel fan-out exclusively for tasks that genuinely require independent sub-task decomposition.

* C) Disable tracing telemetry to reduce payload size and offset the cost increase.

* D) Switch all four subagents to the highest-capability model tier to justify the added cost.

5. An aggregate evaluation score for a multi-step claims-processing agent remains consistently high, yet users report intermittent malformed SQL parameters causing downstream tool failures. Which test layer is specifically designed to catch this class of failure, and why did the aggregate score miss it?

* A) Unit tests would have caught it, since aggregate scores never include local function tests.

* B) Integration tests, which verify schema/data compatibility between two pipeline components (e.g., extraction output feeding a database tool) — aggregate end-to-end scores can mask this because the overall output still "looks" correct despite the intermediate handoff defect.

* C) Functional tests alone would have caught it, since they check exact string equality.

* D) End-to-end tests are irrelevant here since the failure is purely a UI issue.

6. A team places `cache_control: {"type": "ephemeral"}` on a system prompt prefix that includes a dynamically inserted `current_timestamp` value near the top of the prefix. Requests still show high cache-write rates and stale-looking timestamp behavior. What is the architectural issue?

* A) Ephemeral caching requires a minimum of 4 breakpoints to function; only one was configured.

* B) Placing frequently changing data (like a timestamp) inside the cached prefix breaks the exact-prefix-match requirement and/or causes the model to see stale values for the cache's TTL window; volatile data should be placed outside the cached breakpoint.

* C) `cache_control` only applies to tool schemas, never to system prompts.

* D) The cache TTL must be manually reset via the `count_tokens` endpoint before each call.

7. A developer classifies a malformed-JSON schema validation error (caused by Claude generating a string where an integer was expected) as retriable and configures three automatic retries of the identical request. What is wrong with this approach, and what should happen instead?

* A) Nothing is wrong; retrying identical requests always eventually succeeds due to non-determinism.

* B) This is a terminal failure for the identical request — repeating it will likely reproduce the same schema mismatch; the correct approach is to re-prompt with error feedback or route to a fallback rather than blindly retrying the same payload.

* C) The correct fix is to increase `top_p` before retrying.

* D) The correct fix is to disable JSON schema validation entirely to avoid the error.

8. A team wants to enforce that a developer agent can never write outside `/app/workspace/sandbox/`, even if a prompt injection attempts to redirect it to `hosts`. The current implementation relies solely on a system prompt instruction. Why is this insufficient, and what should replace or supplement it?

* A) System prompts are sufficient; the issue must be a bug in the model's instruction-following.

* B) System prompt text is non-deterministic guidance that can be bypassed via prompt injection or hallucination; true enforcement requires a programmatic pre-execution hook validating file paths against a whitelist before the write executes.

* C) The fix is to increase the model's context window so it "remembers" the instruction better.

* D) The fix is to switch to a lower-capability model, which is less likely to attempt unauthorized writes.

9. An enterprise wants to deploy an agent handling both simple intent classification (80% of traffic) and complex multi-document legal synthesis (20% of traffic) while minimizing operating cost without sacrificing quality on the complex slice. What is the correct architecture?

* A) Route 100% of traffic to the highest-capability tier to guarantee quality across both workloads.

* B) Implement dynamic model routing: fast/low-cost tier for the 80% classification slice, high-capability tier for the 20% synthesis slice, validated by evals.

* C) Route 100% of traffic to the fastest, cheapest tier and use retry loops to fix quality issues on the complex slice.

* D) Alternate model tiers randomly per request regardless of task complexity.

10. A security review requires that an agent interacting with both an external weather API and an internal CRM only be permitted to make outbound calls to those two specific endpoints, with no reliance on prompt-level restrictions. What is the correct control layer?

* A) A system prompt instruction listing the two approved endpoints.

* B) Sandbox/platform-level network isolation explicitly whitelisting only the two approved domains, since this is deterministic and cannot be bypassed by prompt injection.

* C) A `PostToolUse` hook that logs violations after the fact but does not block them.

* D) Increasing `max_tokens` to give the model more room to reason about which endpoints are safe.

11. A high-throughput microservice performing real-time text classification is being evaluated for latency and cost optimization. The team must choose between a high-capability reasoning-heavy tier and a fast, low-latency tier. Which choice aligns with production engineering guidance, and why?

* A) The high-capability tier, because higher-capability models always have lower latency in practice.

* B) The fast, low-latency tier, because the workload's capability requirement (simple classification) fits its capability envelope, and using a heavier tier would add unnecessary cost and latency without quality benefit.

* C) Neither tier matters since all Claude models share identical latency profiles.

* D) The high-capability tier, because reasoning mode is mandatory for all production classification tasks.

12. During a regulatory audit, a fintech company must demonstrate identity control, credential storage discipline, action auditing, and configuration lock-down across its Claude Code + MCP integration. Which combination of controls satisfies all four requirements simultaneously?

* A) API keys stored in `CLAUDE.md`, `stdio` transport for all servers, and user-level settings only.

* B) OAuth for user-identity services, environment variables (not hardcoded values) for service credentials, `PostToolUse` hooks for audit logging, and Enterprise Managed Settings for configuration lock-down.

* C) Hardcoded bearer tokens in `.mcp.json`, HTTP transport, and project-level rules only.

* D) `bypassPermissions` mode combined with `disable-model-invocation: true` on all Skills.

---

Topic: 5 Accelerators & IP Contribution

1. A consulting team wants to package a working banking-support agent as a reusable accelerator for future client engagements. Which practice correctly aligns with Agent Template packaging guidelines?

* A) Hardcode each client's credentials and system prompt tone directly into the agent's execution loop for reliability.

* B) Extract client-specific parameters (tone, thresholds, credential references) into external configuration files while keeping the core orchestration loop and tool schemas stable and reusable.

* C) Rewrite the tool schemas and execution loop from scratch for every new client engagement to guarantee correctness.

* D) Store all client secrets directly inside the agent's system prompt for easy auditing.

2. A team is deciding whether to invest time packaging a Model Context Protocol server integration into a full accelerator. The engagement is a one-off build for a legacy system that will never be reused. What is the correct decision per the packaging trade-off guidance?

* A) Always package everything into an accelerator regardless of reuse likelihood, since packaging has no real cost.

* B) Skip full accelerator packaging for this one-off engagement, since packaging overhead is only justified when an asset can be reconfigured and reused across future engagements.

* C) Package only the audit logging component, since audit logs are legally required even for one-off builds.

* D) Package the eval suite only, and skip the agent template and MCP layers entirely.

3. A developer submits a full multi-component enterprise banking application (including proprietary prompts and client-specific business logic) as a pull request to a public reference-implementation repository like the Claude Cookbook. The review stalls indefinitely. What is the root cause?

* A) The repository requires all submissions to include a working CI/CD pipeline, which was missing.

* B) This is a channel mismatch — the repository is designed for focused, self-contained, single- or multi-pattern reference implementations, not full multi-component proprietary applications.

* C) Pull requests to public repositories are always rejected if written in Python.

* D) The submission lacked a signed NDA from the maintaining organization.

4. Before any maintainer begins a technical code review on an externally contributed pattern, which gate must be cleared first, and why does it take precedence over technical review?

* A) A 100% unit test coverage threshold, because maintainers refuse to review any code below this bar.

* B) Licensing and attribution clearance confirming legal authority to contribute code that originated during a client engagement — this precedes technical review because unresolved IP risk cannot be fixed by good code quality.

* C) A benchmark comparing token cost across three different Claude model tiers.

* D) Registration of the contributed prompt templates with an external prompt-management vendor.

5. During due diligence, a developer discovers that a module they intend to contribute upstream contains an unresolved client intellectual property constraint. What is the correct next step?

* A) Strip identifying variable names and submit the code anyway, since obfuscation resolves IP concerns.

* B) Escalate the licensing constraint to the asset owner or engagement manager rather than contributing the code upstream until it is cleared.

* C) Publish the code with an open-source license and an attached disclaimer to shift liability to end users.

* D) Submit the code anonymously under a personal GitHub account to avoid attribution issues.

6. A business sponsor states a goal as "help support agents resolve billing disputes faster." An engineer is asked to translate this into a functional requirement suitable for use as an eval-suite test line. Which statement correctly represents a functional requirement (versus an infrastructure requirement)?

* A) "The platform must guarantee P95 latency under 400ms at 3,000 requests per second."

* B) "The agent must extract the disputed transaction ID, cross-reference the billing policy, and draft a resolution citing the specific policy clause, routing ambiguous cases to a human reviewer."

* C) "All processing must occur within a SOC 2 Type II certified US data center."

* D) "The system must use OAuth2 for all internal service identity propagation."

7. A regulated healthcare deployment skips the formal Requirements-to-Design phase gate and selects a hosting platform before confirming HIPAA and data residency needs. What downstream architectural risk does this create, and what should have happened instead?

* A) No real risk exists, since platform choice can always be changed later without cost.

* B) The team risks an indefensible, non-compliant platform choice; infrastructure requirements (residency, identity, scale, latency) must be captured in the Requirements phase and formally gate the transition into Design/platform selection.

* C) The risk only affects cost estimates, not compliance posture.

* D) This is acceptable practice as long as the Build phase is completed quickly.

8. A team upgrades a production agent's model from a snapshot pinned six months ago to the newest snapshot, using an automated canary process. What is the correct promotion pattern, and why is pinning explicit snapshot IDs (rather than moving aliases) important in the first place?

* A) Route 100% of traffic immediately to the new snapshot since newer models are always strictly better; pinning is only a cosmetic convention.

* B) Route a fraction of traffic to the candidate snapshot, compare its eval-suite score against the pinned baseline, and promote or roll back automatically; pinning explicit snapshot IDs prevents upstream model updates from silently altering production behavior without a controlled rollback path.

* C) Skip evaluation entirely since canary deployments are inherently safe.

* D) Replace the pinned snapshot ID with a moving alias to simplify long-term maintenance.

9. A European bank requires strict EU-only data residency for a Claude-powered assistant. The team is evaluating Microsoft Foundry as a hosting option. Which detail determines whether this requirement is satisfied?

* A) All Microsoft Foundry models satisfy EU residency automatically regardless of hosting configuration.

* B) Only Azure-hosted Foundry models satisfy the requirement, because inference executes end-to-end within Azure's infrastructure; Anthropic-hosted Foundry models do not, since inference runs on Anthropic's infrastructure instead.

* C) EU residency is only achievable via the first-party Anthropic API with a custom system prompt.

* D) Foundry cannot support any EU compliance requirement under any configuration.

10. A multi-component architecture connects a public-facing API, a Claude Code research task that fetches external web content, and an MCP server with direct database write access. A security reviewer flags that the MCP server has broad, unscoped write permissions even though the public API layer is tightly locked down. Why does this still constitute a critical finding?

* A) It doesn't matter, since the public API entry point is the only relevant attack surface.

* B) A multi-component system is only as contained as its most privileged seam; an overly permissive MCP server can be reached and exploited if any upstream component (such as the web-fetching task) is manipulated via indirect prompt injection.

* C) MCP servers are inherently immune to permission escalation regardless of configuration.

* D) This is only a concern if the API layer also lacks OAuth.

11. An integration seam between a Claude Code agent and a legacy internal service cannot be secured against unvalidated external input using any available programmatic control. What is the correct next step according to deployment best practice?

* A) Ship the integration anyway and rely on the model's judgment to avoid unsafe actions.

* B) Halt deployment of that seam and escalate the unresolved risk to a human owner rather than shipping around an unsecured boundary.

* C) Disable audit logging on that seam to reduce noise until a fix is found.

* D) Grant the legacy service elevated privileges so it can self-correct any bad input it receives.

--- Answer Key & Explanations ---

Topic: 1 MSO Foundations

Question 1: B
Explanation: Best practice is to first try adding targeted worked examples to the cheaper model and re-validate against the eval suite before considering an upgrade to a more expensive tier.

Question 2: B
Explanation: An oversized initial payload is rejected before generation starts; a mid-generation overflow returns a truncated response with a distinct context-exceeded stop reason — these require different handling logic.

Question 3: B
Explanation: Autoregressive sampling causes non-determinism in phrasing even when meaning is correct; tests should validate structure/semantics, not exact string equality.

Question 4: C
Explanation: Dynamic model routing sends high-volume simple tasks to a cheap/fast tier and escalates only the complex minority to a high-capability tier, validated by evals.

Question 5: B
Explanation: Tool Use / structured output JSON schemas constrain generation at the API level, eliminating unreliable freeform conversational text.

Question 6: B
Explanation: Worked examples let a smaller model match a larger model's structural accuracy, making it the more cost-effective choice when eval scores are equivalent.

Question 7: B
Explanation: Streaming suits interactive real-time UX, the Message Batches API suits large non-urgent offline jobs, and synchronous calls suit short backend responses with no waiting user.

Question 8: B
Explanation: The Python SDK's `AsyncAnthropic` class provides non-blocking async/await execution, directly resolving thread-blocking issues under concurrent load.

Question 9: B
Explanation: Lowering temperature reduces but does not mathematically eliminate variance; tests should still rely on structural/numeric invariants rather than exact prose matching.

Question 10: B
Explanation: For a single, non-reused, straightforward task, zero-shot prompting with a synchronous call is the minimally sufficient and most cost-effective configuration.

Question 11: B
Explanation: Concrete worked examples pin down exact output shape far more reliably than expanding descriptive instructional text alone.

Topic: 2 Production-Grade Prompting, Agents & Tool Use

Question 1: B
Explanation: Filtering/summarizing large tool outputs at the application layer before reinjecting them into context prevents window exhaustion without requiring a model tier change.

Question 2: A
Explanation: Thinking blocks (including redacted ones) carry cryptographic signatures; the API rejects requests where they've been altered or dropped, so they must be returned unmodified.

Question 3: B
Explanation: Irreversible, state-changing tool calls require a Human-in-the-Loop checkpoint regardless of how well-specified the tool's schema is.

Question 4: A
Explanation: Partial JSON fragments in `content_block_delta` events are not valid JSON until `content_block_stop` fires; parsing must be deferred until then.

Question 5: B
Explanation: Explicit inclusion/exclusion criteria in tool descriptions give Claude clear disambiguation boundaries when tool purposes overlap.

Question 6: A
Explanation: The Anthropic API's MCP Connector only supports remote Streamable HTTP servers; local `stdio` servers must be managed client-side rather than through the API connector.

Question 7: B
Explanation: The `document` content block type natively handles PDF layout and structure, avoiding the overhead and information loss of rasterizing pages into images.

Question 8: B
Explanation: Subagents start with a clean context window and do not automatically inherit parent skills; required skills must be explicitly declared on the subagent's own configuration.

Question 9: B
Explanation: When steps are enumerable, inputs are constrained, and guardrails/observability matter most, a deterministic Workflow is the correct architecture rather than an autonomous Agent.

Question 10: B
Explanation: Claude Managed Agents store state server-side, making them currently ineligible for HIPAA BAA or ZDR coverage; PHI workloads must use the Agent SDK or a raw API loop on a BAA-covered configuration.

Question 11: B
Explanation: Uploading the image once via the Files API (or a stable reference) avoids re-transmitting the full Base64 payload on every turn, cutting network payload size and latency.

Topic: 3 Claude Code, MCP & Integration

Question 1: B
Explanation: Enterprise-level deny rules in `managed-settings.json` deterministically override allow rules and even bypass modes at every configuration tier.

Question 2: B
Explanation: Shareable Skills/plugins must use project-relative paths; embedding a machine-specific absolute path breaks installation on any other developer's machine.

Question 3: B
Explanation: `stdio` transport spawns a local subprocess per machine; teammates lacking the required local runtime (e.g., Node/npx) cannot launch that subprocess, causing failures.

Question 4: B
Explanation: Once a secret is committed, it remains recoverable from git history indefinitely; the only real fix is rotating/revoking the credential, not just replacing the string in a later commit.

Question 5: B
Explanation: An oversized `CLAUDE.md` dilutes the relative weight of any single instruction; large/specialized content should move to scoped rules files or on-demand Skills.

Question 6: B
Explanation: A `PreToolUse` hook that inspects arguments and can exit with code 2 provides deterministic, code-level enforcement that prompt-level instructions cannot guarantee.

Question 7: B
Explanation: Setting `defer_loading: true` in the `mcp_toolset` configuration delays full tool schema loading into context until actually needed, cutting upfront token overhead.

Question 8: B
Explanation: Claude Enterprise on AWS Marketplace is explicitly not FedRAMP authorized; only Bedrock GovCloud, C4G via Palantir, or GCP Vertex AI Assured Workloads satisfy FedRAMP High.

Question 9: B
Explanation: `PostToolUse` hooks fire deterministically after execution and are enforced by the client environment, so the model itself cannot alter, skip, or hallucinate the resulting audit log.

Question 10: B
Explanation: Findings directly verifiable from the diff should be trusted, while unproven runtime behavior claims should be treated as hypotheses requiring empirical verification before action.

Question 11: B
Explanation: Setting `disable-model-invocation: true` in a Skill's frontmatter restricts it to explicit slash-command invocation only, preventing automatic model-triggered execution.

Topic: 4 Production Engineering, Evals & Security

Question 1: B
Explanation: Judge calibration against human-labeled ground truth is required to eliminate scoring bias and drift before an LLM-as-a-judge can be trusted as a production gate.

Question 2: B
Explanation: HTTP 429 is transient and retriable with backoff; a context-length error is structural/terminal and requires a fallback strategy (e.g., chunking), not blind retries.

Question 3: B
Explanation: This is an indirect prompt injection from untrusted fetched content; the fix is enforcing strict untrusted-input boundaries and scoped tool action permissions.

Question 4: B
Explanation: Multi-agent fan-out multiplies cost and latency; it should be reserved only for tasks genuinely requiring independent decomposition, and telemetry should guide the rollback decision.

Question 5: B
Explanation: Integration tests specifically verify schema/data compatibility between pipeline steps — a defect there can be invisible to an aggregate end-to-end quality score.

Question 6: B
Explanation: Volatile data (like timestamps) inside a cached prefix breaks exact-prefix matching and/or causes stale data to be served for the cache's TTL; volatile fields should sit outside the cached breakpoint.

Question 7: B
Explanation: A schema mismatch caused by the model's own output is a terminal failure for that exact payload; the fix is re-prompting with feedback or falling back, not blind retries.

Question 8: B
Explanation: Prompt text is non-deterministic and bypassable via injection; true enforcement requires a deterministic pre-execution hook validating paths against an explicit whitelist.

Question 9: B
Explanation: Dynamic model routing sends the high-volume simple workload to a fast/cheap tier and reserves the high-capability tier for the complex minority, validated by evals.

Question 10: B
Explanation: Network egress restrictions must be enforced at the sandbox/platform level via explicit whitelisting, since this cannot be bypassed by prompt injection unlike prompt-level instructions.

Question 11: B
Explanation: A fast, low-latency tier fits the capability envelope of simple classification tasks; using a heavier reasoning tier adds cost and latency without a corresponding quality gain.

Question 12: B
Explanation: OAuth for user identity, environment variables for service credentials, `PostToolUse` hooks for audit logging, and Enterprise Managed Settings for lock-down together satisfy all four regulatory requirements.

Topic: 5 Accelerators & IP Contribution

Question 1: B
Explanation: Proper Agent Template packaging extracts client-specific details into external configuration while keeping the core execution loop and schemas stable and reusable.

Question 2: B
Explanation: Packaging overhead is only justified when an asset will be reused across future engagements; a genuine one-off build should skip full accelerator packaging.

Question 3: B
Explanation: Submitting a full proprietary multi-component application to a repository built for focused, self-contained reference patterns creates a channel mismatch that stalls review.

Question 4: B
Explanation: Licensing/attribution clearance must happen before technical review, since unresolved IP risk cannot be remediated through code quality improvements.

Question 5: B
Explanation: Unresolved IP constraints must be escalated to the asset owner or engagement manager; the code should not be contributed upstream until cleared.

Question 6: B
Explanation: A functional requirement is a clear, checkable behavioral statement usable directly as an eval-suite test line; the other options describe infrastructure (latency, residency, identity) requirements.

Question 7: B
Explanation: Infrastructure requirements (residency, identity, scale, latency) must be captured during the Requirements phase and formally gate platform selection in Design to avoid indefensible, non-compliant choices.

Question 8: B
Explanation: Canary traffic splitting against a pinned baseline score enables safe promotion/rollback; pinning explicit snapshot IDs prevents silent behavioral drift from upstream model updates.

Question 9: B
Explanation: On Microsoft Foundry, only Azure-hosted models keep inference entirely within Azure's infrastructure boundary, satisfying EU residency; Anthropic-hosted Foundry models do not.

Question 10: B
Explanation: A system is only as secure as its most privileged seam; an overly permissive MCP server remains exploitable if any upstream component is compromised via indirect injection, regardless of how locked-down the public API is.

Question 11: B
Explanation: When a seam cannot be programmatically secured, deployment must halt and escalate to a human owner rather than shipping around the unresolved risk.