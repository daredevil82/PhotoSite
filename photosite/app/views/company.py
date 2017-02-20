from __future__ import absolute_import

from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from app.permissions import IsAdministrator
from app.models.user import Company
from app.serializers.user import CompanySerializer
from app.views import AbstractView

@permission_classes((IsAdministrator, ))
class CompanyListView(AbstractView):
    def __init__(self):
        super().__init__()

    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many = True)
        return Response(serializer.data)

    # TODO: implement way for administrator to create a new Company record
    def post(self, request):
        pass


@permission_classes((IsAdministrator, ))
class CompanyDetailView(AbstractView):
    def __init__(self):
        super().__init__()

    def get(self, request, company_id):
        try:
            company = Company.objects.get(pk = company_id)
            serializer = CompanySerializer(company)
            return Response(serializer.data)
        except Company.DoesNotExist as e:
            self.log.error('Company ID [{}] does not exist'.format(company_id))
            return self.error_response('Company ID [{}] does not exist'.format(company_id))
