from django.shortcuts import render, redirect
from .forms import ContractForm
from .models import Contract
from django.http import JsonResponse
from docusign_esign import (ApiClient, EnvelopesApi, Document,Signer,
                             SignHere, Tabs, Recipients,
                               EnvelopeDefinition,EnvelopeViewRecipientSettings,
                               EnvelopeViewRequest,EnvelopeViewSettings,
                               EnvelopeViewDocumentSettings,EnvelopeViewTemplateSettings,EnvelopeViewTaggerSettings)
import base64
import os
from Rastave import settings

def create_contract(request):
    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.sender = request.user  # گیرنده را به عنوان کاربر وارد شده تنظیم کنید
            contract.save()

            # تبدیل فایل سند به Base64
            with open(contract.document.path, 'rb') as file:
                doc_b64 = base64.b64encode(file.read()).decode('ascii')

            # تنظیمات DocuSign API
            api_client = ApiClient()
            api_client.set_base_path(settings.DOCUSIGN['BASE_URL'])
            api_client.set_default_header("Authorization", f"Bearer {settings.DOCUSIGN['ACCESS_TOKEN']}")

            # تعریف سند
            document = Document(
                document_base64=doc_b64,
                name=contract.title,
                file_extension=contract.document.name.split('.')[-1],
                document_id="1"
            )

            # تعریف امضاکننده
            signer = Signer(
                email=contract.recipient_email,

                recipient_id="1",
                routing_order="1"
            )

            # تنظیم محل امضا
            sign_here = SignHere(
                anchor_string="**signature_1**",  # باید این متن در سند وجود داشته باشد
                anchor_units="pixels",
                anchor_y_offset="10",
                anchor_x_offset="20"
            )
            signer.tabs = Tabs(sign_here_tabs=[sign_here])

            recipients = Recipients(signers=[signer])

            # ایجاد Envelope
            envelope_definition = EnvelopeDefinition(
                email_subject="Please sign this document",
                documents=[document],
                recipients=recipients,
                status="sent"  # ارسال به DocuSign
            )

            envelopes_api = EnvelopesApi(api_client)
            account_id = settings.DOCUSIGN['ACCOUNT_ID']
            results = envelopes_api.create_envelope(account_id=account_id, envelope_definition=envelope_definition)

            # ذخیره اطلاعات Envelope در پایگاه داده
            contract.envelope_id = results.envelope_id
            contract.status = "sent"
            contract.save()

            return JsonResponse({"message": "Contract sent successfully", "envelope_id": results.envelope_id}, status=200)

    else:
        form = ContractForm()
    return render(request, 'send_contract.html', {'form': form})

def sender_view(request, envelope_id):
    """ایجاد لینک Sender View برای مدیریت Envelope"""
    try:
        # تنظیمات مربوط به DocuSign
        api_client = ApiClient()
        api_client.set_base_path(settings.DOCUSIGN['BASE_URL'])
        api_client.set_default_header("Authorization", f"Bearer {settings.DOCUSIGN['ACCESS_TOKEN']}")

        # ساخت Envelope View Request
        view_request = EnvelopeViewRequest(
            return_url=settings.DOCUSIGN['RETURN_URL'],  # URL بازگشت
            view_access="envelope",
            settings=EnvelopeViewSettings(
                starting_screen="recipientAndDocuments",
                send_button_action="send",
                show_back_button="false",
                back_button_action="previousPage",
                show_header_actions="false",
                show_discard_action="false",
                lock_token="",
                recipient_settings=EnvelopeViewRecipientSettings(
                    show_edit_recipients="false",
                    show_contacts_list="false"
                ),
                document_settings=EnvelopeViewDocumentSettings(
                    show_edit_documents="false",
                    show_edit_document_visibility="false",
                    show_edit_pages="false"
                ),
                tagger_settings=EnvelopeViewTaggerSettings(
                    palette_sections="default",
                    palette_default="custom"
                ),
                template_settings=EnvelopeViewTemplateSettings(
                    show_matching_templates_prompt="true"
                )
            )
        )

        # ارسال درخواست به DocuSign برای ایجاد لینک Sender View
        envelope_api = EnvelopesApi(api_client)
        sender_view = envelope_api.create_sender_view(
            account_id=settings.DOCUSIGN['ACCOUNT_ID'],
            envelope_id=envelope_id,
            envelope_view_request=view_request
        )

        # بازگرداندن لینک ایجاد شده
        return JsonResponse({"url": sender_view.url}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)