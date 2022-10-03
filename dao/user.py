from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_all(self):
        return self.session.query(User).all()

    def get_by_username(self, username):
        return self.session.query(User).filter(User.username==username).one()

    def create(self, data):
        res = User(**data)
        self.session.add(res)
        self.session.commit()
        return res

    def delete(self, uid):
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()

    def update(self, data):

        user = self.get_one(data.get('id'))
        user = {k: data.get(k, v) for k, v in user.items()}

        self.session.add(user)
        self.session.commit()