"use client";

import { useState } from "react";

type AnalysisResult = {
  language: string;
  time_complexity: string;
  time_expression: string;
  space_complexity: string;
  limitations: string[];
};

const examples = [
  {
    label: "Linear search",
    complexity: "O(n)",
    code: `def linear_search(numbers, target):
    for i in range(n):
        print(i)
`,
  },
  {
    label: "Nested loops",
    complexity: "O(n²)",
    code: `def nested_loops(n):
    for i in range(n):
        for j in range(n):
            print(i, j)
`,
  },
  {
    label: "Constant work",
    complexity: "O(1)",
    code: `def get_first(numbers):
    result = numbers[0]
    return result
`,
  },
];

const complexityLevels = [
  { name: "Constant", notation: "O(1)", width: "12%" },
  { name: "Logarithmic", notation: "O(log n)", width: "26%" },
  { name: "Linear", notation: "O(n)", width: "43%" },
  { name: "Quadratic", notation: "O(n²)", width: "68%" },
  { name: "Exponential", notation: "O(2ⁿ)", width: "94%" },
];

export default function Home() {
  const [code, setCode] = useState(
    `def process_numbers(n):
    numbers = list(range(n))

    for i in range(n):
        print(numbers[i])
`,
  );

  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  async function analyzeCode() {
    if (!code.trim()) {
      setError("Write or paste some Python code before analyzing.");
      setResult(null);
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("/api/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          code,
          language: "python",
        }),
      });

      const data: unknown = await response.json();

      if (!response.ok) {
        const message =
          typeof data === "object" &&
          data !== null &&
          "detail" in data
            ? String(data.detail)
            : "The analysis could not be completed.";

        throw new Error(message);
      }

      if (
        typeof data !== "object" ||
        data === null ||
        !("time_complexity" in data) ||
        !("space_complexity" in data) ||
        !("time_expression" in data) ||
        !("limitations" in data)
      ) {
        throw new Error("The API returned an unexpected response.");
      }

      setResult(data as AnalysisResult);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong while analyzing your code.",
      );
    } finally {
      setLoading(false);
    }
  }

  function selectExample(exampleCode: string) {
    setCode(exampleCode);
    setResult(null);
    setError("");
  }

  async function copyCode() {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1800);
    } catch {
      setError("Unable to copy code. Please copy it manually.");
    }
  }

  function clearCode() {
    setCode("");
    setResult(null);
    setError("");
  }

  const lineCount = Math.max(code.split("\n").length, 1);

  return (
    <main className="app-shell">
      <header className="site-header">
        <a className="brand" href="/" aria-label="AnalyseComplexite home">
          <span className="brand-mark" aria-hidden="true">
            <span />
            <span />
            <span />
          </span>

          <span className="brand-name">
            Analyse<span>Complexite</span>
          </span>
        </a>

        <nav className="header-nav" aria-label="Main navigation">
          <a href="#workspace">Analyzer</a>
          <a href="#complexity-guide">Complexity guide</a>
        </nav>

        <div className="header-status">
          <span className="status-dot" />
          <span>Python analyzer</span>
        </div>
      </header>

      <section className="hero-section">
        <div className="hero-copy">
          <div className="eyebrow">
            <span className="eyebrow-line" />
            ALGORITHM ANALYSIS TOOL
          </div>

          <h1>
            Understand your
            <br />
            algorithm&apos;s <span>growth.</span>
          </h1>

          <p className="hero-description">
            Explore time and space complexity with a clear,
            code-first workspace. Analyze your Python algorithms
            and understand how their cost grows with input size.
          </p>

          <div className="hero-actions">
            <a href="#workspace" className="primary-button">
              Analyze your code
              <span aria-hidden="true">↘</span>
            </a>

            <a href="#complexity-guide" className="text-button">
              Explore Big O <span aria-hidden="true">→</span>
            </a>
          </div>

          <div className="hero-trust">
            <span className="trust-icon" aria-hidden="true">✓</span>
            <span>Static analysis</span>
            <span className="trust-separator" />
            <span>No code execution</span>
          </div>
        </div>

        <div
          className="hero-visual"
          aria-hidden="true"
        >
          <div className="visual-orbit visual-orbit-one" />
          <div className="visual-orbit visual-orbit-two" />

          <div className="visual-globe">
            <div className="globe-grid globe-grid-horizontal" />
            <div className="globe-grid globe-grid-vertical" />
            <div className="globe-highlight" />
          </div>

          <div className="visual-node node-one" />
          <div className="visual-node node-two" />
          <div className="visual-node node-three" />

          <div className="floating-label label-top">
            <span className="floating-label-dot" />
            TIME COMPLEXITY
            <strong>O(n)</strong>
          </div>

          <div className="floating-label label-bottom">
            <span className="floating-label-dot green" />
            SPACE COMPLEXITY
            <strong>O(n)</strong>
          </div>

          <div className="visual-coordinate">
            INPUT <span>→</span> ANALYSIS <span>→</span> INSIGHT
          </div>
        </div>
      </section>

      <section className="workspace-section" id="workspace">
        <div className="section-heading">
          <div>
            <div className="section-kicker">THE WORKSPACE</div>
            <h2>From code to complexity.</h2>
            <p>
              Submit an algorithm and let the analyzer estimate its
              time and auxiliary space complexity.
            </p>
          </div>

          <div className="language-badge">
            <span className="python-dot">●</span>
            Python 3
            <span className="badge-divider" />
            Static analysis
          </div>
        </div>

        <div className="workspace-grid">
          <section className="editor-card" aria-label="Python code editor">
            <div className="editor-topbar">
              <div className="editor-file">
                <span className="file-icon" aria-hidden="true">
                  PY
                </span>

                <div>
                  <strong>algorithm.py</strong>
                  <span>Python source file</span>
                </div>
              </div>

              <div className="editor-actions">
                <button
                  type="button"
                  className="subtle-button"
                  onClick={copyCode}
                  aria-label="Copy source code"
                >
                  {copied ? "Copied ✓" : "Copy code"}
                </button>

                <button
                  type="button"
                  className="subtle-button"
                  onClick={clearCode}
                >
                  Clear
                </button>
              </div>
            </div>

            <div className="editor-content">
              <div className="line-numbers" aria-hidden="true">
                {Array.from({ length: lineCount }, (_, index) => (
                  <span key={index}>{index + 1}</span>
                ))}
              </div>

              <label className="sr-only" htmlFor="python-code">
                Python source code
              </label>

              <textarea
                id="python-code"
                className="code-input"
                spellCheck={false}
                autoCapitalize="off"
                autoCorrect="off"
                autoComplete="off"
                aria-describedby="editor-help"
                value={code}
                onChange={(event) => {
                  setCode(event.target.value);
                  setError("");
                  setResult(null);
                }}
                placeholder={"def algorithm(n):\n    ..."}
              />
            </div>

            <div className="editor-footer">
              <span id="editor-help">
                {lineCount} lines <span className="footer-separator">·</span>{" "}
                Python
              </span>

              <span>Input size: n</span>
            </div>

            <div className="editor-bottom">
              <div className="editor-hint">
                <span className="hint-icon" aria-hidden="true">i</span>
                <span>
                  Uses static analysis. Your code is not executed.
                </span>
              </div>

              <button
                type="button"
                className="analyze-button"
                onClick={analyzeCode}
                disabled={loading}
              >
                {loading ? (
                  <>
                    <span className="loading-spinner" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    Analyze algorithm
                    <span aria-hidden="true">↗</span>
                  </>
                )}
              </button>
            </div>
          </section>

          <aside className="examples-card">
            <div className="examples-heading">
              <div className="section-kicker">GET STARTED</div>
              <h3>Try an example</h3>
              <p>
                Load a sample algorithm into the editor to explore
                the analyzer.
              </p>
            </div>

            <div className="example-list">
              {examples.map((example, index) => (
                <button
                  type="button"
                  className="example-item"
                  key={example.label}
                  onClick={() => selectExample(example.code)}
                >
                  <span className="example-number">
                    {String(index + 1).padStart(2, "0")}
                  </span>

                  <span className="example-info">
                    <strong>{example.label}</strong>
                    <span>Expected pattern: {example.complexity}</span>
                  </span>

                  <span className="example-arrow" aria-hidden="true">
                    ↗
                  </span>
                </button>
              ))}
            </div>

            <div className="examples-note">
              <span className="note-icon" aria-hidden="true">✳</span>
              <p>
                <strong>Keep in mind</strong>
                <br />
                The analyzer supports a subset of Python. Some
                statements and function calls may not be supported.
              </p>
            </div>
          </aside>
        </div>
      </section>

      <section
        className="results-section"
        aria-labelledby="results-title"
        aria-live="polite"
      >
        <div className="results-heading">
          <div>
            <div className="section-kicker">ANALYSIS REPORT</div>
            <h2 id="results-title">Your results.</h2>
          </div>

          <span className={`report-status ${result ? "complete" : ""}`}>
            <span className="status-dot" />
            {result ? "Analysis complete" : "Awaiting analysis"}
          </span>
        </div>

        {error && (
          <div className="error-message" role="alert">
            <span className="error-symbol" aria-hidden="true">!</span>
            <div>
              <strong>Analysis unsuccessful</strong>
              <p>{error}</p>
            </div>
          </div>
        )}

        {result ? (
          <div className="results-content">
            <div className="metrics-grid">
              <article className="metric-card">
                <div className="metric-label">
                  <span className="metric-icon time-icon" aria-hidden="true">
                    ↗
                  </span>
                  TIME COMPLEXITY
                </div>

                <div className="metric-value">
                  {result.time_complexity}
                </div>

                <p>Estimated growth of execution cost</p>

                <div className="metric-bottom">
                  <span className="metric-indicator" />
                  Big O notation
                </div>
              </article>

              <article className="metric-card">
                <div className="metric-label">
                  <span className="metric-icon space-icon" aria-hidden="true">
                    ◫
                  </span>
                  SPACE COMPLEXITY
                </div>

                <div className="metric-value">
                  {result.space_complexity}
                </div>

                <p>Estimated auxiliary space growth</p>

                <div className="metric-bottom">
                  <span className="metric-indicator green-indicator" />
                  Big O notation
                </div>
              </article>
            </div>

            <article className="expression-card">
              <div className="expression-heading">
                <div>
                  <div className="section-kicker">COST MODEL</div>
                  <h3>Time cost expression</h3>
                </div>

                <span className="expression-language">
                  PYTHON · ESTIMATE
                </span>
              </div>

              <div className="expression-value">
                <span>T(n)</span>
                <span>=</span>
                <code>{result.time_expression}</code>
              </div>

              <p>
                This polynomial is an estimate from the analyzer&apos;s
                supported cost model. It is not a benchmark of actual
                execution time.
              </p>
            </article>

            {result.limitations.length > 0 && (
              <article className="limitations-card">
                <div className="limitations-title">
                  <span aria-hidden="true">ⓘ</span>
                  <h3>Analysis scope &amp; limitations</h3>
                </div>

                <ul>
                  {result.limitations.map((limitation, index) => (
                    <li key={`${limitation}-${index}`}>{limitation}</li>
                  ))}
                </ul>
              </article>
            )}
          </div>
        ) : (
          <div className="empty-results">
            <div className="empty-illustration" aria-hidden="true">
              <div className="empty-illustration-line line-a" />
              <div className="empty-illustration-line line-b" />
              <div className="empty-illustration-line line-c" />
              <span>ƒ(n)</span>
            </div>

            <h3>Your analysis starts here.</h3>
            <p>
              Submit Python code above to see its estimated time
              complexity, space complexity, and cost expression.
            </p>

            <span className="empty-caption">
              RESULTS WILL APPEAR AFTER ANALYSIS
            </span>
          </div>
        )}
      </section>

      <section
        className="complexity-section"
        id="complexity-guide"
      >
        <div className="complexity-intro">
          <div className="section-kicker">A QUICK REFERENCE</div>
          <h2>
            Think in terms of
            <br />
            <span>growth, not seconds.</span>
          </h2>
          <p>
            Big O describes how an algorithm&apos;s cost scales as the
            input grows. It helps compare algorithms independently
            of a particular machine.
          </p>

          <a href="#workspace" className="text-button">
            Analyze an algorithm <span aria-hidden="true">→</span>
          </a>
        </div>

        <div className="complexity-chart-card">
          <div className="chart-header">
            <div>
              <strong>Common complexity classes</strong>
              <span>Illustrative reference</span>
            </div>

            <span className="chart-n-label">GROWTH →</span>
          </div>

          <div className="complexity-list">
            {complexityLevels.map((level, index) => (
              <div className="complexity-row" key={level.notation}>
                <div className="complexity-row-info">
                  <span className="complexity-index">
                    {String(index + 1).padStart(2, "0")}
                  </span>

                  <span className="complexity-name">{level.name}</span>

                  <code>{level.notation}</code>
                </div>

                <div
                  className="complexity-track"
                  role="img"
                  aria-label={`${level.name} reference bar`}
                >
                  <div
                    className={`complexity-bar complexity-bar-${index + 1}`}
                    style={{ width: level.width }}
                  />
                </div>
              </div>
            ))}
          </div>

          <p className="chart-disclaimer">
            Reference only. These bars illustrate relative growth
            classes; they are not calculated from your submitted code.
          </p>
        </div>
      </section>

      <section className="closing-section">
        <div className="closing-mark" aria-hidden="true">
          {"{ }"}
        </div>

        <div>
          <div className="section-kicker">BETTER CODE STARTS WITH CLARITY</div>
          <h2>Understand the cost. Improve the algorithm.</h2>
        </div>

        <a href="#workspace" className="closing-link">
          Back to workspace <span aria-hidden="true">↑</span>
        </a>
      </section>

      <footer className="site-footer">
        <a className="brand footer-brand" href="/">
          <span className="brand-mark" aria-hidden="true">
            <span />
            <span />
            <span />
          </span>

          <span className="brand-name">
            Analyse<span>Complexite</span>
          </span>
        </a>

        <p>Made for curious minds and better algorithms.</p>

        <span className="footer-copyright">
          © {new Date().getFullYear()} AnalyseComplexite
        </span>
      </footer>
    </main>
  );
}