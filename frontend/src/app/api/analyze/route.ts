import { NextResponse } from "next/server";

const API_URL =
  process.env.ANALYSE_API_URL ?? "http://127.0.0.1:8000";

export async function POST(request: Request) {
  let body: unknown;

  try {
    body = await request.json();
  } catch {
    return NextResponse.json(
      { detail: "The request body must contain valid JSON." },
      { status: 400 },
    );
  }

  if (
    typeof body !== "object" ||
    body === null ||
    !("code" in body) ||
    typeof body.code !== "string" ||
    body.code.trim().length === 0
  ) {
    return NextResponse.json(
      { detail: "Please provide Python code to analyze." },
      { status: 400 },
    );
  }

  try {
    const response = await fetch(`${API_URL}/analyze`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        code: body.code,
        language: "python",
      }),
      cache: "no-store",
      signal: AbortSignal.timeout(30_000),
    });

    const data = await response.json();

    return NextResponse.json(data, {
      status: response.status,
    });
  } catch {
    return NextResponse.json(
      {
        detail:
          "Unable to reach the analysis API. Make sure the FastAPI backend is running on port 8000.",
      },
      { status: 503 },
    );
  }
}
