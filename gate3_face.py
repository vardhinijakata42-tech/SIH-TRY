
def biometric_demo(selfie):
    if selfie is None:
        return {
            "status": "READY",
            "detail": "Consent-based face verification/liveness integration placeholder.",
            "review": False,
        }
    return {
        "status": "READY",
        "detail": "Selfie received for demo UI. Connect an approved, consent-based liveness/face-verification provider for production.",
        "review": False,
    }
