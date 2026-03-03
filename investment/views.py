from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from .forms import InvestmentForm
from openai import OpenAI


# ==============================
# INVESTMENT PAGE
# ==============================
def investment_view(request):

    if request.method == "POST":
        form = InvestmentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('investment')
    else:
        form = InvestmentForm()

    return render(request, 'investment.html', {'form': form})


# ==============================
# MITRA AI VIEW (FINAL WORKING)
# ==============================
# ==============================
# MITRA AI VIEW (FINAL WORKING)
# ==============================
def mitra_ai(request):

    if request.method != "POST":
        return JsonResponse({"reply": "Invalid request method."})

    user_message = request.POST.get("message")

    if not user_message or user_message.strip() == "":
        return JsonResponse({"reply": "Ask me something 😊"})

    try:
        client = OpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )

        system_prompt = """
You are MoneyMitra AI, a financial assistant for Indian students.

IMPORTANT RULES:
- Use only the exact numbers provided by the user.
- Never modify numbers.
- If user says 900, it means 900 (NOT 9000).
- Repeat investment values before giving advice.
- Be accurate over creative.
- Keep response clear and practical.
- Currency is Indian Rupees (₹).
- If information is incomplete, ask a follow-up question.
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            temperature=0.3,  # lower = more accurate
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
        )

        ai_text = response.choices[0].message.content.strip()

        return JsonResponse({"reply": ai_text})

    except Exception as e:
        print("AI Error:", e)
        return JsonResponse({
            "reply": "Mitra AI is temporarily unavailable."
        })