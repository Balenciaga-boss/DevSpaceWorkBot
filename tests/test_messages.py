from devspace_bot.messages import APPLICATION_SUCCESS_TEXT


def test_application_success_text_says_request_was_sent_for_estimate():
    assert "успешно отправлена на оценку" in APPLICATION_SUCCESS_TEXT
    assert "скоро свяжемся" in APPLICATION_SUCCESS_TEXT
