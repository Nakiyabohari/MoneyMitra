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
# MITRA AI VIEW
# ==============================
def mitra_ai(request):

    if request.method != "POST":
        return JsonResponse({"reply": "Invalid request method."})

    user_message = request.POST.get("amount")

    if not user_message:
        return JsonResponse({"reply": "Ask me something 😊"})

    try:
        client = OpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are Mitra AI, a smart and friendly Indian financial assistant.
                    Speak naturally like ChatGPT.
                    Keep replies helpful, practical and slightly conversational.
                    Avoid robotic formatting.
                    """
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=0.9   # 🔥 makes it more human
        )

        ai_text = response.choices[0].message.content.strip()

        return JsonResponse({"reply": ai_text})

    except Exception as e:
        print("AI Error:", e)
        return JsonResponse({
            "reply": "Mitra AI is temporarily unavailable."
        })