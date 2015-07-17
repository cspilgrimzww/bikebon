__author__ = 'cspilgrim'
from itsdangerous import TimedJSONWebSignatureSerializer as Serialize

class BKUser(db.Model):
    __tablename__ = 'bk_user'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), index=True)
    user_password_hash = db.Column(db.String(128))
    user_phone = db.Column(db.String(32))
    user_balance = db.Column(db.Float)
    user_deposit = db.Column(db.Float)

    def generate_auth_token(self,expiration):
        s = Serialize(current_app.config['SECRET_KEY'],
                      expires_in=expiration)
        return s.dumps({'id',self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serialize(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def to_json(self):
        json_user = {
            'username':self.user_name,
            'phone':self.user_phone,
            'balance':self.user_balance,
            'deposit':self.user_deposit
        }
        return json_user
