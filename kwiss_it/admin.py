from django.contrib import admin
from kwiss_it.models import Picture, UserDescription, UserPicture, UserLastSeen, Score, State, Category, Score_Category, QuestionType, Question, Answer, ReportType, Report, DiscordRole

admin.site.register(Picture)
admin.site.register(UserDescription)
admin.site.register(UserPicture)
admin.site.register(UserLastSeen)
admin.site.register(Score)
admin.site.register(State)
admin.site.register(Category)
admin.site.register(Score_Category)
admin.site.register(QuestionType)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(ReportType)
admin.site.register(Report)
admin.site.register(DiscordRole)