from voting.models import Vote
from tagging.models import Tag

class Backend:
    def create_user_matrix(self, users, items):
        user_item_matrix = {}
        for user in users:
            votes_for_user = Vote.objects.get_for_user_in_bulk(items, user)
            user_item_matrix[user.id] = votes_for_user

        return user_item_matrix

    def create_item_tag_matrix(self, user, tagged_items):
        item_tag_matrix = {}
        for item in tagged_items:
            item_tag_matrix[item] = Tag.objects.get_for_object(item)

        return item_tag_matrix

    def get_user_tags(self, user):
        return Tag.objects.get_for_object(user)

