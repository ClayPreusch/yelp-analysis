import json
import matplotlib.pyplot as plt

# Load the business.json file
with open('yelp_dataset/business.json', 'r', encoding='utf-8') as f:
    businesses = [json.loads(line) for line in f]

# Load the review.json file
with open('yelp_dataset/review.json', 'r', encoding='utf-8') as f:
    reviews = [json.loads(line) for line in f]

# Load the user.json file
with open('yelp_dataset/user.json', 'r', encoding='utf-8') as f:
    users = [json.loads(line) for line in f]

# Get the number of businesses, reviews, and users
num_businesses = len(businesses)
num_reviews = len(reviews)
num_users = len(users)
print(f"Number of businesses: {num_businesses}")
print(f"Number of reviews: {num_reviews}")
print(f"Number of users: {num_users}")

# Get the distribution of business ratings
rating_counts = {}
for business in businesses:
    rating = business['stars']
    if rating in rating_counts:
        rating_counts[rating] += 1
    else:
        rating_counts[rating] = 1

print("Business rating distribution:")
for rating, count in rating_counts.items():
    print(f"{rating} stars: {count}")

# Get the distribution of review lengths
review_lengths = [len(review['text']) for review in reviews]
print(f"Average review length: {sum(review_lengths) / len(review_lengths)}")

# Analyze the differences between Elite and non-Elite users
elite_users = [user for user in users if 'elite' in user and len(user['elite']) > 0]
non_elite_users = [user for user in users if 'elite' not in user or len(user['elite']) == 0]

print(f"Number of Elite users: {len(elite_users)}")
print(f"Number of non-Elite users: {len(non_elite_users)}")

elite_review_counts = [user['review_count'] for user in elite_users]
non_elite_review_counts = [user['review_count'] for user in non_elite_users]

print("Average review count:")
print(f"Elite users: {sum(elite_review_counts) / len(elite_users)}")
print(f"Non-Elite users: {sum(non_elite_review_counts) / len(non_elite_users)}")

elite_avg_stars = sum([user['average_stars'] for user in elite_users]) / len(elite_users)
non_elite_avg_stars = sum([user['average_stars'] for user in non_elite_users]) / len(non_elite_users)

print("Average star rating:")
print(f"Elite users: {elite_avg_stars:.2f}")
print(f"Non-Elite users: {non_elite_avg_stars:.2f}")

# Analyze the relationship between Elite status and review helpfulness
elite_useful = sum([user['useful'] for user in elite_users])
non_elite_useful = sum([user['useful'] for user in non_elite_users])

elite_funny = sum([user['funny'] for user in elite_users])
non_elite_funny = sum([user['funny'] for user in non_elite_users])

elite_cool = sum([user['cool'] for user in elite_users])
non_elite_cool = sum([user['cool'] for user in non_elite_users])

print("Total helpfulness votes:")
print(f"Elite users - Useful: {elite_useful}, Funny: {elite_funny}, Cool: {elite_cool}")
print(f"Non-Elite users - Useful: {non_elite_useful}, Funny: {non_elite_funny}, Cool: {non_elite_cool}")

# Analyze the relationship between business ratings and Elite vs. non-Elite reviews
elite_business_ratings = []
non_elite_business_ratings = []

for review in reviews:
    business_id = review['business_id']
    business = next((b for b in businesses if b['business_id'] == business_id), None)
    if business:
        user_id = review['user_id']
        user = next((u for u in users if u['user_id'] == user_id), None)
        if user:
            if 'elite' in user and len(user['elite']) > 0:
                elite_business_ratings.append(business['stars'])
            else:
                non_elite_business_ratings.append(business['stars'])

print("Average business rating:")
print(f"Elite reviewer businesses: {sum(elite_business_ratings) / len(elite_business_ratings):.2f}")
print(f"Non-Elite reviewer businesses: {sum(non_elite_business_ratings) / len(non_elite_business_ratings):.2f}")

# Visualize the data
plt.figure(figsize=(12, 6))

# Business rating distribution
plt.subplot(1, 2, 1)
plt.bar(rating_counts.keys(), rating_counts.values())
plt.xlabel("Business Rating")
plt.ylabel("Count")
plt.title("Business Rating Distribution")

# Review length distribution
plt.subplot(1, 2, 2)
plt.hist(review_lengths, bins=20)
plt.xlabel("Review Length")
plt.ylabel("Count")
plt.title("Distribution of Review Lengths")

plt.tight_layout()
plt.show()