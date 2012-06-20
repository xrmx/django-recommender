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

    # TESTS
    def add_vote_for_user(self, movie, user, vote):
        Vote.objects.record_vote(movie, user, vote)

    def add_tag(self, model, tag):
        Tag.objects.add_tag(model, tag)

    def print_matrix(self, users, items):
        item_names = [str(item)[0:7] for item in items]
        print '\t' + '\t'.join(item_names)
        for other in users:
            votes_for_user = Vote.objects.get_for_user_in_bulk(items, other)
            votes = []
            for item in items:
                if item.id in votes_for_user:
                    votes.append('%d' % votes_for_user[item.id].vote)
                else:
                    votes.append(' ')
            print str(other)[0:7] +'\t'+ '\t'.join(votes)
