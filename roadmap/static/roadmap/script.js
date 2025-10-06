document.querySelectorAll('.complete-form').forEach(form => {
    form.addEventListener('submit', function(e) {
        const topicCard = this.closest('.topic-card');
        topicCard.style.transition = 'all 0.5s ease';
        topicCard.style.opacity = '0';
        topicCard.style.transform = 'translateX(100px)';
    });
});
window.addEventListener('DOMContentLoaded', () => {
    const topicCards = document.querySelectorAll('.topic-card');
    topicCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
});