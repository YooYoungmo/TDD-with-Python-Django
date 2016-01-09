신규 사이트 프로비저닝
============================
## 필요 패키지
* nginx
* python 2.7
* Git
* pip
* virtualenv

Ubuntu에서 실행 방법 예:
sudo apt-get install nginx git python-pip
sudo pip install virtualenv

## Nginx 가상 호스트 설정
*nginx.template.conf 참고 

## Upstart Job
* gunicorn-upstart.template.conf 참고

## 폴더 구조
/home/username
ㄴsites
	ㄴsitename
		ㄴdatabase
		ㄴsource
		ㄴstatic
		ㄴvirtualenv
