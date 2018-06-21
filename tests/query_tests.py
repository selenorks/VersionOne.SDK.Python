
from testtools import TestCase
from testtools.content import text_content
from testtools.matchers import GreaterThan, LessThan, Contains, StartsWith, EndsWith

import v1pysdk
from .common_test_server import PublicTestServerConnection

class TestV1Query(TestCase):
    def test_select_story_as_generic_asset(self):
        """Queries up to 5 story assets"""
        with PublicTestServerConnection.getV1Meta() as v1:
            querySucceeded=True
            size=0
            item=None
            try:
                items = v1.AssetType.select('Name').where(Name='Story').page(size=5)
                item = items.first() #triggers actual query to happen
                size = len(items)
            except:
                querySucceeded=False

            # test assumes there is at least 1 Story on the test server
            self.assertTrue(querySucceeded)
            self.assertThat(size,LessThan(6))
            self.assertThat(size,GreaterThan(0))

    def test_select_story(self):
        """Queries up to 5 stories"""
        with PublicTestServerConnection.getV1Meta() as v1:
            querySucceeded=True
            size=0
            item=None
            try:
                items = v1.Story.select('Name').page(size=5)
                item = items.first() #triggers actual query to happen
                size = len(items)
            except:
                querySucceeded=False

            # test assumes there is at least 1 Story on the test server
            self.assertTrue(querySucceeded)
            self.assertThat(size,LessThan(6))
            self.assertThat(size,GreaterThan(0))

    def test_select_epic(self):
        """Queries up to 5 Epics, called Portfolios in the GUI.
           In order to create a new Story, we must be able to query for an Epic we want to put it under,
           and pass that returned Epic object as the Super of the new Story.  This confirms the Epic query
           part always works.
        """
        with PublicTestServerConnection.getV1Meta() as v1:
            querySucceeded=True
            size=0
            item=None
            try:
                items = v1.Epic.select('Name').page(size=5)
                item = items.first() #triggers actual query to happen
                size = len(items)
            except:
                querySucceeded=False

            # test assumes there is at least 1 Portfolio Item on the test server
            self.assertTrue(querySucceeded)
            self.assertThat(size,LessThan(6))
            self.assertThat(size,GreaterThan(0))


    def test_select_scope(self):
        """Queries up to 5 Scopes, called Projects in the GUI.
           In order to create a new Story, we must be able to query for a Scope we want to put it under,
           and pass that returned Scope object as the Scope of the new Story.  This confirms the Scope query
           part always works.
        """
        with PublicTestServerConnection.getV1Meta() as v1:
            querySucceeded=True
            size=0
            item=None
            try:
                items = v1.Scope.select('Name').page(size=5)
                item = items.first() #triggers actual query to happen
                size = len(items)
            except:
                querySucceeded=False

            # test assumes there is at least 1 Project on the test server
            self.assertTrue(querySucceeded)
            self.assertThat(size,LessThan(6))
            self.assertThat(size,GreaterThan(0))

    def test_select_task(self):
        """Queries up to 5 Tasks.
        """
        with PublicTestServerConnection.getV1Meta() as v1:
            querySucceeded=True
            size=0
            item=None
            try:
                items = v1.Task.select('Name').page(size=5)
                item = items.first() #triggers actual query to happen
                size = len(items)
            except:
                querySucceeded=False

            # test assumes there is at least 1 Task on the test server
            self.assertTrue(querySucceeded)
            self.assertThat(size,LessThan(6))
            self.assertThat(size,GreaterThan(0))

    def test_non_default_query(self):
        """Queries an attribute that's not retrieved by default from a Story so it will requery for the specific
           attribute that was requested.
        """
        with PublicTestServerConnection.getV1Meta() as v1:
            failedFetchCreateDate = False
            failedFetchName = False
            s = v1.Story.select('Name').page(size=1)
            try:
                junk = s.CreateDate # fetched on demand, not default
            except:
                failedFetchCreateDate = True

            self.assertFalse(failedFetchCreateDate)

            try:
                junk = s.Name # fetched by default on initial query
            except:
                failedFetchName = True

            self.assertFalse(failedFetchName)


    def test_sum_query(self):
        """Queries for a summation of values of a numeric field (Actuals.Value) across a set of assests (Tasks).
        """
        with PublicTestServerConnection.getV1Meta() as v1:
            foundActuals=False
            exceptionReached=False
            try:
                tasks = v1.Task.select('Name','Actuals.Value.@Sum').page(size=30)
                tasks.first() #perform the actual query
                if len(tasks) <= 0:
                    self.skipTest("Test server contains no Tasks")
                    return
                else:
                    for t in tasks:
                        if 'Actuals.Value.@Sum' in t.data:
                            foundActuals=True
                            break
            except:
                exceptionReached=True
            else:
                if not foundActuals:
                    self.skipTest("Test server Tasks contained no Actuals.Value's")
                    return


            self.assertFalse(exceptionReached)

# This should work, but doesn't for some reason.  It doesn't find any results from the find command
#    def test_find_query(self):
#        """Queries for the first story, then does a server-side find on a portion of the name to see if 
#           any results are returned.
#        """
#        searchName=""
#        exceptionReached=False
#        with PublicTestServerConnection.getV1Meta() as v1:
#            item = None
#            size = 0
#            name = ""
#            items = None
#            try:
#                items = v1.Story.select('Name').page(size=40)
#                item = items.first() #triggers actual query to happen
#                size = len(items)
#            except:
#                self.skipTest("Unable to query for a Story object -- Story query test should have failed")
#                return
#            else:
#                if size <= 0:
#                    self.skipTest("Test Server contains no Stories")
#                    return
#
#            for i in items:
#                if len(i.Name) >= 2:
#                    name = i.Name
#                    self.addDetail('item-name', text_content(name))
#                    break
#
#            if len(name) < 2:
#                self.skipTest("Test Server contains too many single character named stories")
#                return
#
#            # make a search term that's just one character shorter
#            searchName = name[:-1]
#            self.addDetail('search-name', text_content(searchName))
#
#        with PublicTestServerConnection.getV1Meta() as v1:
#            findItems = None
#            findItem = None
#            size = 0
#            firstName = ""
#            try:
#                findItems = v1.Story.select('Name').find(text=searchName, field='Name')
#                findItem = findItems.first() #actually run the query
#                size = len(findItems)
#                firstName = findItem.Name
#            except Exception as e:
#                raise e
#                #exceptions here are almost always because the query failed to work right
#                exceptionReached=True
#            else:
#                # at the very least we should have found the one we based the search string on
#                self.assertThat(size, GreaterThan(0))
#                # results need to contain the string we searched for
#                self.assertThat(firstName, Contains(searchName))
#
#            self.assertFalse(exceptionReached)
#
