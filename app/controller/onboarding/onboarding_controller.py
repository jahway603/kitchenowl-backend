from app.helpers import validate_args
from flask import jsonify, Blueprint
from app.models import User, Token
from .schemas import OnboardSchema

onboarding = Blueprint('onboarding', __name__)


@onboarding.route('', methods=['GET'])
def isOnboarding():
    onboarding = User.count() == 0
    return jsonify({"onboarding": onboarding})


@onboarding.route('', methods=['POST'])
@validate_args(OnboardSchema)
def onboard(args):
    if User.count() > 0:
        return jsonify({'msg': "Onboarding not allowed"}), 403

    username = args['username'].lower()
    user = User.create(username, args['password'], args['name'], admin=True)

    device = "Unkown"
    if "device" in args:
        device = args['device']

    # Create refresh token
    refreshToken, refreshModel = Token.create_refresh_token(user, device)

    # Create first access token
    accesssToken, _ = Token.create_access_token(user, refreshModel)

    return jsonify({
        'access_token': accesssToken,
        'refresh_token': refreshToken
    })
